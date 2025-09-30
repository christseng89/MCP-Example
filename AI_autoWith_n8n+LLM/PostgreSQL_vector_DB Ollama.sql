-- 一次啟用（若未安裝）
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS doc_ollama;
CREATE TABLE doc_ollama (
  id         BIGSERIAL PRIMARY KEY,
  "text"     TEXT        NOT NULL,
  metadata   JSONB       NOT NULL DEFAULT '{}'::jsonb,
  embedding  VECTOR(768) NOT NULL           -- ← 改成你的模型維度
);

CREATE INDEX doc_ollama_embedding_ivfflat
  ON doc_ollama USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX doc_ollama_metadata_gin
  ON doc_ollama USING gin (metadata);
