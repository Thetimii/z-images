import runpod
import torch
from diffusers import AutoPipelineForText2Image
import base64
import io

import os

# Load model globally so it stays in VRAM between requests
# The model will be loaded from the cache populated by builder/model_fetcher.py
print("Loading model...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "Tongyi-MAI/Z-Image-Turbo", 
    torch_dtype=torch.float16, 
    variant="fp16"
).to("cuda")
print("Model loaded successfully.")

def handler(job):
    """
    Handler function that will be used to process jobs.
    """
    job_input = job['input']
    
    # Security: Check for API Key
    # The API_KEY env var should be set in the RunPod Template or Environment Variables
    expected_api_key = os.environ.get("API_KEY")
    if expected_api_key:
        input_api_key = job_input.get("api_key")
        if input_api_key != expected_api_key:
            return {"error": "Unauthorized: Invalid or missing 'api_key'"}

    # helper to validate input
    if 'prompt' not in job_input:
        return {"error": "Missing 'prompt' in input"}
        
    prompt = job_input['prompt']
    
    # Optional parameters with defaults
    num_inference_steps = job_input.get('num_inference_steps', 1) # Z-Image-Turbo is fast!
    guidance_scale = job_input.get('guidance_scale', 0.0)
    
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
