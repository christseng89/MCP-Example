-- Enable pgvector once per database
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table (adjust VECTOR dimension to your embedding model)
CREATE TABLE IF NOT EXISTS public.documents (
  id        BIGSERIAL PRIMARY KEY,
  "text"    TEXT    NOT NULL,                -- chunk text
  metadata  JSONB   NOT NULL DEFAULT '{}'::jsonb,
  embedding VECTOR(1536) NOT NULL            -- e.g., 1536 for text-embedding-3-small
);

-- Useful indexes
CREATE INDEX IF NOT EXISTS documents_embedding_ivfflat
  ON public.documents USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

CREATE INDEX IF NOT EXISTS documents_metadata_gin
  ON public.documents USING gin (metadata);

-- Vector search with optional JSONB filter; returns top-N by cosine similarity
CREATE OR REPLACE FUNCTION public.match_documents(
  query_embedding VECTOR(1536),
  match_count     INT  DEFAULT 10,
  filter          JSONB DEFAULT '{}'::jsonb
)
RETURNS TABLE (
  id         BIGINT,
  "text"     TEXT,
  metadata   JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
STABLE
AS $$
#variable_conflict use_column
BEGIN
  RETURN QUERY
  SELECT
    d.id,
    d."text",
    d.metadata,
    (1 - (d.embedding <=> query_embedding))::float AS similarity
  FROM public.documents AS d
  WHERE (filter IS NULL OR filter = '{}'::jsonb OR d.metadata @> filter)
  ORDER BY d.embedding <=> query_embedding
  LIMIT COALESCE(match_count, 10);
END;
$$;

-- After large ingests, run: ANALYZE public.documents;

-- Example query to check for duplicates based on filename
SELECT count (*) FROM public.documents WHERE metadata->>'filename' = 'Nvidia10K_2025.pdf';