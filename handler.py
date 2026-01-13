import runpod
import torch
from diffusers import ZImagePipeline
import base64
import io
import os
from datetime import datetime
from supabase import create_client, Client

# Load model globally using ZImagePipeline
print("Loading Z-Image-Turbo model...")
pipe = ZImagePipeline.from_pretrained(
    "Tongyi-MAI/Z-Image-Turbo", 
    torch_dtype=torch.bfloat16,
    use_safetensors=True
).to("cuda")
print("Model loaded successfully.")

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")  # Use service role key for storage access

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized.")
else:
    print("WARNING: Supabase credentials not found. Images will only return as base64.")

def handler(job):
    """
    Handler function for RunPod serverless inference.
    """
    job_input = job['input']
    job_id = job.get('id', 'unknown')
    
    # Security: Check for API Key
    expected_api_key = os.environ.get("API_KEY")
    if expected_api_key:
        input_api_key = job_input.get("api_key")
        if input_api_key != expected_api_key:
            return {"error": "Unauthorized: Invalid or missing 'api_key'"}

    # Validate input
    if 'prompt' not in job_input:
        return {"error": "Missing 'prompt' in input"}
        
    prompt = job_input['prompt']
    user_id = job_input.get('user_id')  # Optional: track which user generated this
    
    # Z-Image-Turbo optimal parameters
    num_inference_steps = job_input.get('num_inference_steps', 8)
    guidance_scale = job_input.get('guidance_scale', 0.0)
    
    # Run inference
    print(f"Generating image for prompt: {prompt}")
    with torch.inference_mode():
        image = pipe(
            prompt=prompt, 
            num_inference_steps=num_inference_steps, 
            guidance_scale=guidance_scale
        ).images[0]
    
    # Convert to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    
    # If Supabase is configured, upload the image
    if supabase:
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{job_id[:8]}.png"
            storage_path = f"images/{filename}"
            
            # Upload to Supabase Storage
            print(f"Uploading to Supabase: {storage_path}")
            supabase.storage.from_("generated-images").upload(
                path=storage_path,
                file=image_bytes,
                file_options={"content-type": "image/png"}
            )
            
            # Get public URL
            public_url = supabase.storage.from_("generated-images").get_public_url(storage_path)
            
            # Save metadata to database
            supabase.table("generated_images").insert({
                "prompt": prompt,
                "image_url": public_url,
                "storage_path": storage_path,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "user_id": user_id,
                "job_id": job_id
            }).execute()
            
            print(f"Image saved successfully: {public_url}")
            
            return {
                "success": True,
                "image_url": public_url,
                "storage_path": storage_path,
                "prompt": prompt
            }
            
        except Exception as e:
            print(f"Error uploading to Supabase: {str(e)}")
            # Fallback to base64 if upload fails
            img_str = base64.b64encode(image_bytes).decode('utf-8')
            return {
                "success": False,
                "error": f"Supabase upload failed: {str(e)}",
                "image_base64": img_str,
                "format": "png"
            }
    else:
        # Fallback: return base64 if Supabase not configured
        img_str = base64.b64encode(image_bytes).decode('utf-8')
        return {
            "image": img_str,
            "format": "png",
            "note": "Supabase not configured, returning base64"
        }

runpod.serverless.start({"handler": handler})
