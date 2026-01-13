# Z-Image-Turbo on RunPod Serverless

This repository deploys the **Tongyi-MAI/Z-Image-Turbo** model (6B parameters, S3-DiT architecture) on [RunPod Serverless](https://runpod.io).

## Features
- **Fast Cold Starts**: Model weights baked into Docker image
- **API Key Security**: Environment-variable based authentication
- **Optimized for Speed**: Uses `bfloat16` and ZImagePipeline with 8-step inference
- **PyTorch 2.5.1**: Latest CUDA 12.4 support

## Requirements
- **GPU**: RTX 4090 (24GB) or A100 recommended
- **Container Disk**: 15GB+
- **VRAM**: 14-16GB minimum

## Deployment Instructions

1. **Create RunPod Serverless Endpoint**:
   - Use GitHub integration: `https://github.com/Thetimii/z-images`
   - Branch: `master`
   - Dockerfile path: `Dockerfile`

2. **Configure Endpoint**:
   - **GPU**: RTX 4090 (24GB)
   - **Container Disk**: 15GB+
   - **Environment Variables**: 
     - `API_KEY` = `your_secret_password`

3. **Wait for Build**: First build takes ~10-15 minutes (downloads PyTorch 2.5.1 and model weights)

## Testing

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "input": {
      "prompt": "A cinematic shot of a futuristic city with neon lights",
      "api_key": "your_secret_password",
      "num_inference_steps": 8,
      "guidance_scale": 0.0
    }
  }'
```

## Z-Image-Turbo Parameters

- **num_inference_steps**: 8-10 (optimal, higher is worse)
- **guidance_scale**: Must be 0.0 (turbo model)
- **torch_dtype**: bfloat16 (for memory efficiency)

## Technical Details

- **Base Image**: NVIDIA CUDA 12.4.1 with cuDNN
- **PyTorch**: 2.5.1 (required for ZImagePipeline)
- **Diffusers**: Installed from source (latest ZImagePipeline support)
