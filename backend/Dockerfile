FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/home/app/.cache/huggingface

WORKDIR /app

# Install dependencies first (cached layer), read from pyproject.toml
COPY pyproject.toml ./
RUN python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))" > requirements.txt \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .
RUN useradd --create-home --uid 10001 app && chown -R app:app /app
USER app

# Pre-download the bge-m3 tokenizer used by the chunker (avoids a download at first ingest).
RUN python -c "from tokenizers import Tokenizer; Tokenizer.from_pretrained('BAAI/bge-m3')"

EXPOSE 8000
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
