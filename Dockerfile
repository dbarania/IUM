FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git libgl1 libglib2.0-0 libgomp1 procps python3-pip python3.10-venv \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv hf

ENV HF_HOME=/models \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1
RUN mkdir -p /models

RUN --mount=type=cache,target=/root/.cache/huggingface \
    hf download VisteK528/facebook-bart-cnn-ium-v3 --cache-dir /models && \
    hf download facebook/bart-large-cnn --cache-dir /models && \
    hf download facebook/nllb-200-distilled-600M --cache-dir /models

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt

COPY src/ .
RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]