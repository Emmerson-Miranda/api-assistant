# OpenAPI Ingestion Service

Accepts raw OpenAPI specs (JSON/YAML), parses endpoints, and extracts semantic descriptions.

[Ensure that you have created an account with OpenAI.](https://platform.openai.com/login)

[OpenAI embedding models.](https://platform.openai.com/docs/guides/embeddings/embedding-models)


## Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

Run server

```bash
uvicorn app.main:app --reload
```

Curl with happy path

Example 1

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"spec": {"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"}, "paths": {}}}'
```

Example 2

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/text" \
  --data-binary @../client_script/specifications/billing/customer_api.yaml
```

## Docker (build and run)

```bash
# Build Docker image
docker build -t ingestion-api .

# Run the container (connects to external PostgreSQL)
docker run --env-file .env -p 8000:8000 ingestion-api

```