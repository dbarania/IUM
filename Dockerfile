FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# 1. System dependencies (Rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git libgl1 libglib2.0-0 libgomp1 procps python3-pip python3.10-venv \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv hf

# 2. Setup environment and directory for models FIRST
# We put this ABOVE the app code so it's cached independently
ENV HF_HOME=/models \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1
RUN mkdir -p /models

# 3. Download models using a cache mount
# This ensures that even if you rebuild the image, the 'models' folder 
# persists on the host build-cache and won't re-download from the web.
RUN --mount=type=cache,target=/root/.cache/huggingface \
    hf download VisteK528/facebook-bart-cnn-ium-v3 --cache-dir /models && \
    hf download facebook/bart-large-cnn --cache-dir /models && \
    hf download facebook/nllb-200-distilled-600M --cache-dir /models

WORKDIR /app

# 4. Requirements (Change occasionally)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt

# 5. Application Code (Changes constantly)
# By placing this last, code changes take < 1 second to rebuild.
COPY src/ .
RUN mkdir -p /app/logs

EXPOSE 8000

# Using 'fastapi dev' is great for development as it includes --reload
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]