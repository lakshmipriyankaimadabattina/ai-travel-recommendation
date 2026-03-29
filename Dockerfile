FROM python:3.11-slim as builder
WORKDIR /app

# Step 1: Install spacy with its typer first
RUN pip install --no-cache-dir "typer==0.9.4" "spacy==3.7.4"

# Step 2: Install fastapi without its CLI (which causes the conflict)
RUN pip install --no-cache-dir --no-deps "fastapi==0.111.0"

# Step 3: Install everything else except spacy and fastapi
RUN pip install --no-cache-dir \
    "starlette==0.37.2" \
    "uvicorn[standard]==0.29.0" \
    "motor==3.3.2" \
    "pymongo==4.6.3" \
    "pydantic==2.6.4" \
    "pydantic-settings==2.2.1" \
    "scikit-learn==1.4.2" \
    "pandas==2.2.1" \
    "numpy==1.26.4" \
    "requests==2.31.0" \
    "python-dotenv==1.0.1" \
    "pytest==8.1.1" \
    "httpx==0.27.0" \
    "pytest-asyncio==0.23.6" \
    "email-validator" \
    "python-multipart" \
    "orjson" \
    "ujson" \
    "jinja2"

# Step 4: Download spacy model directly
RUN pip install --no-cache-dir \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

