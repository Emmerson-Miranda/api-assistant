-- Enable the pgvector extension (must be installed on the DB server)
CREATE EXTENSION IF NOT EXISTS vector;

-- Table: apis
CREATE TABLE apis (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    UNIQUE(name, version)
);

-- Table: api_endpoints
CREATE TABLE api_endpoints (
    id SERIAL PRIMARY KEY,
    api_id INTEGER NOT NULL REFERENCES apis(id) ON DELETE CASCADE,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    summary TEXT,
    description TEXT,
    UNIQUE(api_id, method, path)
);

-- Table: embeddings
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    endpoint_id INTEGER NOT NULL REFERENCES api_endpoints(id) ON DELETE CASCADE,
    embedding vector(1536) NOT NULL, -- assumes OpenAI’s text-embedding-3-small
    model TEXT NOT NULL,             -- e.g., 'text-embedding-3-small'
    part TEXT NOT NULL,              -- e.g., 'text', 'title', 'description'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(endpoint_id, model, part)
);

-- Optional index for vector similarity search
-- You can use one of the supported index types, e.g.:
-- - ivfflat (fast, needs ANALYZE and fixed lists)
-- - hnsw (hierarchical, efficient for large-scale)
-- Below: IVF index (example)
CREATE INDEX embeddings_embedding_idx
ON embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
