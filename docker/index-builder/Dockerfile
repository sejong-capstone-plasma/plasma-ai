FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ANONYMIZED_TELEMETRY=False

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        chromadb==1.5.1 \
        pypdf==5.1.0 \
        pydantic==2.11.7 \
        pydantic-settings==2.10.1 \
        python-dotenv==1.1.1

COPY app /workspace/app
COPY scripts /workspace/scripts

RUN mkdir -p /workspace/data/knowledge/raw \
             /workspace/data/index/chroma

CMD ["python", "-m", "scripts.build_index"]
