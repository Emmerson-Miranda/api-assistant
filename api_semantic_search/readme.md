# Semantic Search API (AI Agent via FastAPI)

Accepts user queries, converts them to embeddings, and retrieves the most relevant endpoints using cosine similarity.

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

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" \
  -d '{"query": "create a new invoice"}'
```


## Docker (build and run)

```bash
# Build Docker image
docker build -t semantic-search-api .

# Run the container (connects to external PostgreSQL)
docker run --env-file .env -p 8000:8000 semantic-search-api

```