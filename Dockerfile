FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install runpod diffusers transformers accelerate huggingface_hub

WORKDIR /

# Copy the fetcher
COPY builder/model_fetcher.py .

# IMPORTANT: If the model is gated, your coder needs to pass the HF_TOKEN here
# Or ensure the model is public.
RUN python model_fetcher.py

COPY handler.py .
CMD [ "python", "-u", "/handler.py" ]
