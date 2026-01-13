FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Install PyTorch 2.5.1 with CUDA 12.4 support
RUN pip3 install torch==2.5.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install diffusers from source (required for ZImagePipeline)
RUN pip3 install git+https://github.com/huggingface/diffusers.git

# Install other dependencies
RUN pip3 install runpod transformers accelerate sentencepiece protobuf supabase

WORKDIR /

# Copy the fetcher
COPY builder/model_fetcher.py .

# Download model during build
RUN python3 model_fetcher.py

COPY handler.py .
CMD [ "python3", "-u", "/handler.py" ]
