-- ============================
-- UFC Fights → PGVector set-up
-- ============================

-- 0) Schema & extensions
CREATE SCHEMA IF NOT EXISTS ufc;
SET search_path = ufc, public;

CREATE EXTENSION IF NOT EXISTS vector;   -- pgvector
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- for text search helpers

-- 1) Staging table for raw CSV (Date comes as YYYY/MM/DD, so load as TEXT first)
DROP TABLE IF EXISTS ufc.fights_staging;

CREATE TABLE ufc.fights_staging (
  RedFighter                    TEXT,
  BlueFighter                   TEXT,
  RedOdds                       INTEGER,
  BlueOdds                      INTEGER,
  RedExpectedValue              NUMERIC,
  BlueExpectedValue             NUMERIC,
  "Date"                        TEXT,      -- load as TEXT, convert after COPY
  "Location"                    TEXT,
  "Country"                     TEXT,
  Winner                        TEXT,
  TitleBout                     BOOLEAN,
  WeightClass                   TEXT,
  Gender                        TEXT,
  NumberOfRounds                INTEGER,

  BlueCurrentLoseStreak         INTEGER,
  BlueCurrentWinStreak          INTEGER,
  BlueDraws                     INTEGER,
  BlueAvgSigStrLanded           NUMERIC,
  BlueAvgSigStrPct              NUMERIC,
  BlueAvgSubAtt                 NUMERIC,
  BlueAvgTDLanded               NUMERIC,
  BlueAvgTDPct                  NUMERIC,
  BlueLongestWinStreak          INTEGER,
  BlueLosses                    INTEGER,
  BlueTotalRoundsFought         INTEGER,
  BlueTotalTitleBouts           INTEGER,
  BlueWinsByDecisionMajority    INTEGER,
  BlueWinsByDecisionSplit       INTEGER,
  BlueWinsByDecisionUnanimous   INTEGER,
  BlueWinsByKO                  INTEGER,
  BlueWinsBySubmission          INTEGER,
  BlueWinsByTKODoctorStoppage   INTEGER,
  BlueWins                      INTEGER,
  BlueStance                    TEXT,
  BlueHeightCms                 NUMERIC,
  BlueReachCms                  NUMERIC,
  BlueWeightLbs                 INTEGER,

  RedCurrentLoseStreak          INTEGER,
  RedCurrentWinStreak           INTEGER,
  RedDraws                      INTEGER,
  RedAvgSigStrLanded            NUMERIC,
  RedAvgSigStrPct               NUMERIC,
  RedAvgSubAtt                  NUMERIC,
  RedAvgTDLanded                NUMERIC,
  RedAvgTDPct                   NUMERIC,
  RedLongestWinStreak           INTEGER,
  RedLosses                     INTEGER,
  RedTotalRoundsFought          INTEGER,
  RedTotalTitleBouts            INTEGER,
  RedWinsByDecisionMajority     INTEGER,
  RedWinsByDecisionSplit        INTEGER,
  RedWinsByDecisionUnanimous    INTEGER,
  RedWinsByKO                   INTEGER,
  RedWinsBySubmission           INTEGER,
  RedWinsByTKODoctorStoppage    INTEGER,
  RedWins                       INTEGER,
  RedStance                     TEXT,
  RedHeightCms                  NUMERIC,
  RedReachCms                   NUMERIC,
  RedWeightLbs                  INTEGER,
  RedAge                        INTEGER,
  BlueAge                       INTEGER,

  LoseStreakDif                 INTEGER,
  WinStreakDif                  INTEGER,
  LongestWinStreakDif           INTEGER,
  WinDif                        INTEGER,
  LossDif                       INTEGER,
  TotalRoundDif                 INTEGER,
  TotalTitleBoutDif             INTEGER,
  KODif                         INTEGER,
  SubDif                        INTEGER,
  HeightDif                     NUMERIC,
  ReachDif                      INTEGER,
  AgeDif                        INTEGER,
  SigStrDif                     NUMERIC,
  AvgSubAttDif                  NUMERIC,
  AvgTDDif                      NUMERIC,

  EmptyArena                    TEXT,
  BMatchWCRank                  INTEGER,
  RMatchWCRank                  INTEGER,
  RWFlyweightRank               INTEGER,
  RWFeatherweightRank           INTEGER,
  RWStrawweightRank             INTEGER,
  RWBantamweightRank            INTEGER,
  RHeavyweightRank              INTEGER,
  RLightHeavyweightRank         INTEGER,
  RMiddleweightRank             INTEGER,
  RWelterweightRank             INTEGER,
  RLightweightRank              INTEGER,
  RFeatherweightRank            INTEGER,
  RBantamweightRank             INTEGER,
  RFlyweightRank                INTEGER,
  RPFPRank                      INTEGER,
  BWFlyweightRank               INTEGER,
  BWFeatherweightRank           INTEGER,
  BWStrawweightRank             INTEGER,
  BWBantamweightRank            INTEGER,
  BHeavyweightRank              INTEGER,
  BLightHeavyweightRank         INTEGER,
  BMiddleweightRank             INTEGER,
  BWelterweightRank             INTEGER,
  BLightweightRank              INTEGER,
  BFeatherweightRank            INTEGER,
  BBantamweightRank             INTEGER,
  BFlyweightRank                INTEGER,
  BPFPRank                      INTEGER,

  BetterRank                    TEXT,        -- 'Red' | 'Blue' | 'neither'
  Finish                        TEXT,
  FinishDetails                 TEXT,
  FinishRound                   INTEGER,
  FinishRoundTime               TEXT,        -- mm:ss
  TotalFightTimeSecs            INTEGER,

  RedDecOdds                    INTEGER,
  BlueDecOdds                   INTEGER,
  RSubOdds                      INTEGER,
  BSubOdds                      INTEGER,
  RKOOdds                       INTEGER,
  BKOOdds                       INTEGER
);

-- 2) Load CSV
-- If running on the SERVER with file accessible to Postgres:
--   adjust the absolute path below.
-- COPY ufc.fights_staging
-- FROM '/absolute/path/to/Test.csv'
-- WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');

-- If running from psql on your laptop, prefer \copy (no superuser needed):
-- \copy ufc.fights_staging FROM 'Test.csv' WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');

-- 3) Normalize Date (CSV is YYYY/MM/DD)
ALTER TABLE ufc.fights_staging
  ALTER COLUMN "Date" TYPE DATE
  USING to_date("Date",'YYYY/MM/DD');

-- 4) Vector table to store JSON row + embedding + FTS
DROP TABLE IF EXISTS ufc.fights_vectors CASCADE;

CREATE TABLE ufc.fights_vectors (
  id         BIGSERIAL PRIMARY KEY,
  raw        JSONB NOT NULL,

  -- Flatten all values into a single text for embeddings & FTS
  content    TEXT GENERATED ALWAYS AS (
               (SELECT string_agg(j.value, ' ' ORDER BY j.key)
                FROM jsonb_each_text(raw) AS j)
             ) STORED,

  embedding  VECTOR(1536),  -- set to your embedding size
  search     TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 5) Full-text index (build now)
CREATE INDEX fights_vectors_search_ix
  ON ufc.fights_vectors
  USING GIN (search);

-- 6) (Optional) Build ANN index AFTER embeddings are populated for faster creation.
--    If you prefer to build now, uncomment the block below.
-- CREATE INDEX fights_vectors_emb_ix
--   ON ufc.fights_vectors
--   USING ivfflat (embedding vector_cosine_ops)
--   WITH (lists = 100);

-- 7) Load rows from staging into vector table
INSERT INTO ufc.fights_vectors (raw)
SELECT to_jsonb(s) FROM ufc.fights_staging AS s;

-- 8) Examples to populate embeddings
--    A) Single row update (for demo)
-- UPDATE ufc.fights_vectors
-- SET embedding = '[0.0123, -0.0045, ...]'::vector
-- WHERE id = 42;

--    B) Bulk upsert from a temp table you fill from your app/ETL
-- CREATE TEMP TABLE _emb (id BIGINT, emb VECTOR(1536));
-- -- INSERT INTO _emb VALUES (1, '[...]'), (2, '[...]'), ...;
-- UPDATE ufc.fights_vectors v
-- SET embedding = e.emb
-- FROM _emb e
-- WHERE v.id = e.id;

--    C) After embeddings are populated, create the ANN index:
-- CREATE INDEX fights_vectors_emb_ix
--   ON ufc.fights_vectors
--   USING ivfflat (embedding vector_cosine_ops)
--   WITH (lists = 100);

-- 9) Quick validation queries

-- Rows loaded
SELECT count(*) AS rows_in_vectors FROM ufc.fights_vectors;

-- Sample rows missing embeddings
SELECT id, left(content, 120) AS preview
FROM ufc.fights_vectors
WHERE embedding IS NULL
LIMIT 10;

-- Full-text search
SELECT id,
       ts_rank(search, plainto_tsquery('english','Rakhmonov')) AS rank,
       left(content, 120) AS preview
FROM ufc.fights_vectors
WHERE search @@ plainto_tsquery('english','Rakhmonov')
ORDER BY rank DESC
LIMIT 10;

-- Vector search (once embeddings are present)
-- SELECT id,
--        1 - (embedding <=> '[...]'::vector) AS cosine_sim,
--        left(content, 120) AS preview
-- FROM ufc.fights_vectors
-- ORDER BY embedding <=> '[...]'::vector
-- LIMIT 10;
