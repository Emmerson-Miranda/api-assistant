-- Enable the pgvector extension (must be installed on the DB server)
CREATE EXTENSION IF NOT EXISTS vector;

-- Table: apis
CREATE TABLE IF NOT EXISTS public.apis
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    version character varying COLLATE pg_catalog."default" NOT NULL,
    spec json NOT NULL,
    uploaded_at timestamp without time zone DEFAULT now(),
    CONSTRAINT apis_pkey PRIMARY KEY (id)
);

-- Table: api_endpoints
CREATE TABLE IF NOT EXISTS public.api_endpoints
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    api_id character varying COLLATE pg_catalog."default" NOT NULL,
    path character varying COLLATE pg_catalog."default" NOT NULL,
    method character varying COLLATE pg_catalog."default" NOT NULL,
    summary text COLLATE pg_catalog."default",
    operation_id character varying COLLATE pg_catalog."default",
    CONSTRAINT api_endpoints_pkey PRIMARY KEY (id),
    CONSTRAINT api_endpoints_api_id_fkey FOREIGN KEY (api_id)
        REFERENCES public.apis (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- Table: embeddings
CREATE TABLE embeddings (
    id character varying COLLATE pg_catalog."default" NOT NULL,
    endpoint_id character varying NOT NULL REFERENCES api_endpoints(id) ON DELETE CASCADE,
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
