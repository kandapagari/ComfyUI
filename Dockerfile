FROM python:3.11-slim

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    gcc \
    musl-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# USER runner:runner
COPY . /code

VOLUME [ "./models:/code/models" ]

WORKDIR /code
EXPOSE 8188

# Install dependencies
RUN pip install uv
RUN uv pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu126 --system
RUN uv pip install -r requirements.txt --system
