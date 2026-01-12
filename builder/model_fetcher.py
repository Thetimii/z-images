import torch
from diffusers import ZImagePipeline

def download_model():
    model_id = "Tongyi-MAI/Z-Image-Turbo"
    
    # Download using ZImagePipeline (CPU-only during build)
    print(f"Downloading {model_id}...")
    ZImagePipeline.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16,
        use_safetensors=True
    )
    print("Download complete!")

if __name__ == "__main__":
    download_model()
