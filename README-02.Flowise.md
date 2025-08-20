# FlowiseAI

---

## 🧾 Install Flowise

```cmd
node --version
  v20.19.4
npm install -g flowise
flowise --version
  flowise/3.0.5 win32-x64 node-v20.19.4
npx flowise start

npm update -g flowise
```

<https://openrouter.ai/>
<https://openrouter.ai/anthropic/claude-3.7-sonnet> => ☰ => Keys (build agents course) => Create

<https://composio.dev/>
<https://old-app.composio.dev/developers> => Apps => All Apps => GoogleCalendar => Create => Auth0
<https://old-app.composio.dev/developers> => Settings => Project Settings => Project API Key (build agents course) => Create => Copy

## Supabase

<https://supabase.com/>

## Local Postgres Vector Extension

<https://github.com/pgvector/pgvector>

- Press Start (Windows key), type:

```type
  x64 Native Tools Command Prompt for VS 2022 (Run as Administrator)
```

- Run Command

```cmd
set "PGROOT=C:\Program Files\PostgreSQL\17"
cd %TEMP%
git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
cd pgvector
nmake /F Makefile.win
nmake /F Makefile.win install

```

```cmd
psql -U postgres
```

```sql test vector
CREATE EXTENSION vector;
   -- CREATE EXTENSION

CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

```

```sql for mspatterns vector
-- In psql, connected to your target DB
CREATE EXTENSION IF NOT EXISTS vector;

-- a) Main table
-- Drop the table if it already exists
DROP TABLE IF EXISTS mspatterns;

-- Create the table with the expected columns
CREATE TABLE mspatterns (
    id bigserial PRIMARY KEY,
    "pageContent" text,          -- document text
    metadata jsonb,              -- extra metadata
    embedding vector(1536)       -- adjust dimension if using text-embedding-3-large (3072)
);


-- (optional) create ANN index after bulk ingest
-- Create the index on the embedding column
CREATE INDEX ON mspatterns
USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100)
```
