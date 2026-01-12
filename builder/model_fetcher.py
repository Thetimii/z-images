import torch
from diffusers import AutoPipelineForText2Image
import os

def download_model():
    model_id = "Tongyi-MAI/Z-Image-Turbo"
    print(f"Downloading model: {model_id}...")
    
    # Download and cache the model
    # We load it once to force the download to the default cache directory
    pipe = AutoPipelineForText2Image.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        variant="fp16",
    )
    print("Model successfully downloaded and cached.")

if __name__ == "__main__":
    download_model()
