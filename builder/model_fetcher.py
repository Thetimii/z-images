import torch
from diffusers import AutoPipelineForText2Image
import os

def download_model():
    model_id = "Tongyi-MAI/Z-Image-Turbo"
    
    # We download in FP16 to save space, but keep it on CPU during build
    print(f"Downloading {model_id}...")
    AutoPipelineForText2Image.from_pretrained(
        model_id, 
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )
    print("Download complete!")

if __name__ == "__main__":
    download_model()
