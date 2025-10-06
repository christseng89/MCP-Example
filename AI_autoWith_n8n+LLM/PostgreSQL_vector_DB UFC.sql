-- ==========================================================
-- 🥊 UFC Fights CSV → PostgreSQL + PGVector Import Pipeline
-- ==========================================================

-- ----------------------------------------------------------
-- 0) Schema & Extensions
-- ----------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS ufc;
SET search_path = ufc, public;

CREATE EXTENSION IF NOT EXISTS vector;   -- pgvector
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- text similarity

-- ----------------------------------------------------------
-- 1) Drop NOT NULL constraints (prepare for CSV import)
-- ----------------------------------------------------------
DO $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT c.table_schema, c.table_name, c.column_name
        FROM information_schema.columns c
        WHERE c.table_schema = 'ufc'
          AND c.table_name  = 'fights_staging'
          AND c.is_nullable = 'NO'
        ORDER BY c.ordinal_position
    LOOP
        EXECUTE format(
            'ALTER TABLE %I.%I ALTER COLUMN %I DROP NOT NULL;',
            rec.table_schema, rec.table_name, rec.column_name
        );
    END LOOP;
END $$;

-- Verify no NOT NULL columns remain
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'ufc'
  AND table_name  = 'fights_staging'
  AND is_nullable = 'NO';

-- ----------------------------------------------------------
-- 2) Create Staging Table (raw CSV import)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS ufc.fights_staging;

CREATE TABLE ufc.fights_staging (
  RedFighter                    TEXT,
  BlueFighter                   TEXT,
  RedOdds                       INTEGER,
  BlueOdds                      INTEGER,
  RedExpectedValue              NUMERIC,
  BlueExpectedValue             NUMERIC,
  "Date"                        TEXT,      -- will convert to DATE later
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

  BetterRank                    TEXT,
  Finish                        TEXT,
  FinishDetails                 TEXT,
  FinishRound                   INTEGER,
  FinishRoundTime               TEXT,
  TotalFightTimeSecs            INTEGER,

  RedDecOdds                    INTEGER,
  BlueDecOdds                   INTEGER,
  RSubOdds                      INTEGER,
  BSubOdds                      INTEGER,
  RKOOdds                       INTEGER,
  BKOOdds                       INTEGER
);

-- ----------------------------------------------------------
-- 3) Import CSV file
-- ----------------------------------------------------------
-- Adjust path for your environment:
-- COPY ufc.fights_staging
-- FROM '/absolute/path/to/Test.csv'
-- WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');

-- OR use psql client method:
-- \copy ufc.fights_staging FROM 'Test.csv' WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');

-- ----------------------------------------------------------
-- 4) Convert Date format (YYYY/MM/DD → DATE)
-- ----------------------------------------------------------
ALTER TABLE ufc.fights_staging
  ALTER COLUMN "Date" TYPE DATE
  USING to_date("Date", 'YYYY/MM/DD');

-- ----------------------------------------------------------
-- 5) Create Vector Table (for embeddings + FTS)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS ufc.fights_vectors CASCADE;

CREATE TABLE ufc.fights_vectors (
    id          BIGSERIAL PRIMARY KEY,
    raw         JSONB NOT NULL,
    content     TEXT,
    embedding   VECTOR(1536),
    search      TSVECTOR,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- Function to flatten JSON values into one string
CREATE OR REPLACE FUNCTION ufc.jsonb_to_text(_json JSONB)
RETURNS TEXT AS $$
BEGIN
    RETURN (
        SELECT string_agg(value, ' ')
        FROM jsonb_each_text(_json)
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to refresh the generated columns (content & search)
CREATE OR REPLACE FUNCTION ufc.refresh_fight_vectors()
RETURNS void AS $$
BEGIN
    UPDATE ufc.fights_vectors
    SET 
        content = ufc.jsonb_to_text(raw),
        search  = to_tsvector('english', ufc.jsonb_to_text(raw))
    WHERE content IS NULL OR search IS NULL;
END;
$$ LANGUAGE plpgsql;

-- Optional: run after data is inserted from staging
INSERT INTO ufc.fights_vectors (raw)
SELECT to_jsonb(s) FROM ufc.fights_staging AS s;

-- Populate flattened text and FTS vector
SELECT ufc.refresh_fight_vectors();

-- ----------------------------------------------------------
-- 6) Create Indexes
-- ----------------------------------------------------------
CREATE INDEX fights_vectors_search_ix
  ON ufc.fights_vectors
  USING GIN (search);

CREATE INDEX fights_vectors_emb_ix
  ON ufc.fights_vectors
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- ----------------------------------------------------------
-- 7) Populate Vector Table from Staging
-- ----------------------------------------------------------
INSERT INTO ufc.fights_vectors (raw)
SELECT to_jsonb(s) FROM ufc.fights_staging AS s;

-- ----------------------------------------------------------
-- 8) Example Embedding Updates
-- ----------------------------------------------------------
-- Single row demo
-- UPDATE ufc.fights_vectors
-- SET embedding = '[0.123, -0.456, ...]'::vector
-- WHERE id = 42;

-- Bulk update
-- CREATE TEMP TABLE _emb (id BIGINT, emb VECTOR(1536));
-- INSERT INTO _emb VALUES (1, '[...]'), (2, '[...]');
-- UPDATE ufc.fights_vectors v
-- SET embedding = e.emb
-- FROM _emb e
-- WHERE v.id = e.id;

-- After embeddings, build ANN index
-- CREATE INDEX fights_vectors_emb_ix
--   ON ufc.fights_vectors
--   USING ivfflat (embedding vector_cosine_ops)
--   WITH (lists = 100);

-- ----------------------------------------------------------
-- 9) Validation Queries
-- ----------------------------------------------------------
SELECT count(*) AS total_loaded FROM ufc.fights_vectors;

SELECT id, left(content, 100) AS preview
FROM ufc.fights_vectors
WHERE embedding IS NULL
LIMIT 5;

SELECT id, ts_rank(search, plainto_tsquery('english', 'Rakhmonov')) AS rank,
       left(content, 120) AS preview
FROM ufc.fights_vectors
WHERE search @@ plainto_tsquery('english', 'Rakhmonov')
ORDER BY rank DESC
LIMIT 10;

-- Example vector similarity query (after embeddings)
-- SELECT id, 1 - (embedding <=> '[...]'::vector) AS cosine_sim,
--        left(content, 120)
-- FROM ufc.fights_vectors
-- ORDER BY embedding <=> '[...]'::vector
-- LIMIT 10;

-- ✅ End of SQL Pipeline

-- Import data to table
-- Create schema if it doesn't exist
```bash
psql -U postgres
```

CREATE SCHEMA IF NOT EXISTS ufc;

-- Ensure PostgreSQL uses it by default
SET search_path = ufc, public;

-- Then run your import
COPY ufc.fights_staging FROM 'C:/Users/samfi/Downloads/ufc-master.csv' WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');
