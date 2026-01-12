import runpod
import torch
from diffusers import ZImagePipeline
import base64
import io
import os

# Load model globally using ZImagePipeline
print("Loading Z-Image-Turbo model...")
pipe = ZImagePipeline.from_pretrained(
    "Tongyi-MAI/Z-Image-Turbo", 
    torch_dtype=torch.bfloat16,
    use_safetensors=True
).to("cuda")
print("Model loaded successfully.")

def handler(job):
    """
    Handler function for RunPod serverless inference.
    """
    job_input = job['input']
    
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
    
    # Z-Image-Turbo optimal parameters
    num_inference_steps = job_input.get('num_inference_steps', 8)  # 8-10 is optimal
    guidance_scale = job_input.get('guidance_scale', 0.0)  # Must be 0.0 for turbo
    
    # Run inference
    with torch.inference_mode():
        image = pipe(
            prompt=prompt, 
            num_inference_steps=num_inference_steps, 
            guidance_scale=guidance_scale
        ).images[0]
    
    # Convert to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return {
        "image": img_str,
        "format": "png"
    }

runpod.serverless.start({"handler": handler})
