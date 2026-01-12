FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

# Set working directory
WORKDIR /

# Install system dependencies if any (none strictly needed for basic run, but good practice to have clean env)
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
# using --no-cache-dir to keep image size slightly smaller
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the builder script -> This step caches the model weights in the image
COPY builder/model_fetcher.py .
RUN python model_fetcher.py

# Copy the handler
COPY handler.py .

# Start the handler
CMD [ "python", "-u", "handler.py" ]
