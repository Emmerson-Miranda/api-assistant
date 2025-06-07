-- Enable the pgvector extension (must be installed on the DB server)
CREATE EXTENSION IF NOT EXISTS vector;

-- Table: apis
CREATE TABLE IF NOT EXISTS public.apis
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    version character varying COLLATE pg_catalog."default" NOT NULL,
    spec json NOT NULL,
    embedding vector(1536) NOT NULL, -- assumes OpenAI’s text-embedding-3-small
    model TEXT NOT NULL,             -- e.g., 'text-embedding-3-small'
    uploaded_at timestamp without time zone DEFAULT now(),
    CONSTRAINT apis_pkey PRIMARY KEY (id)
);

