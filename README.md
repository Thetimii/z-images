# Z-Image-Turbo on RunPod Serverless

This repository contains the code and configuration to deploy the **Tongyi-MAI/Z-Image-Turbo** model on [RunPod Serverless](https://runpod.io).

It features:
- **Fast Cold Starts**: Model weights are baked into the Docker image.
- **API Key Security**: Simple environment-variable based authentication.
- **Optimized Inference**: Uses `torch.float16` and half-precision loading.

## Deployment Instructions

1.  **Fork/Clone** this repository to your GitHub.
2.  **Create a RunPod Serverless Endpoint**:
    - **Container Image**: Use the RunPod GitHub integration or your built Docker image (e.g., `thetimii/z-images:latest`).
    - **GPU**: RTX 4090 (24GB) recommended.
    - **Container Disk**: 10GB+.
3.  **Environment Variables**:
    - Go to your Endpoint Configuration.
    - Add a new variable: `API_KEY` = `your_secret_password` (replace with your own secure key).

## Testing

Once deployed, copy your Endpoint ID and use the following command:

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "input": {
      "prompt": "a futuristic cyberpunk cat, neon lights, 8k",
      "api_key": "your_secret_password"
    }
  }' > output.json
```

The response will contain a `base64` string of the generated image.
