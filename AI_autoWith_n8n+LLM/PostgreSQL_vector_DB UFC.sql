-- -- ==========================================================
-- -- 🥊 UFC Fights CSV → PostgreSQL + PGVector Import Pipeline
-- -- ==========================================================

-- -- ----------------------------------------------------------
-- -- 0) Schema & Extensions
-- -- ----------------------------------------------------------
-- CREATE SCHEMA IF NOT EXISTS ufc;
-- SET search_path = ufc, public;

-- CREATE EXTENSION IF NOT EXISTS vector;   -- pgvector
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- text similarity

-- -- ----------------------------------------------------------
-- -- 1) Drop NOT NULL constraints (prepare for CSV import)
-- -- ----------------------------------------------------------
-- DO $$
-- DECLARE
--     rec RECORD;
-- BEGIN
--     FOR rec IN
--         SELECT c.table_schema, c.table_name, c.column_name
--         FROM information_schema.columns c
--         WHERE c.table_schema = 'ufc'
--           AND c.table_name  = 'fights_staging'
--           AND c.is_nullable = 'NO'
--         ORDER BY c.ordinal_position
--     LOOP
--         EXECUTE format(
--             'ALTER TABLE %I.%I ALTER COLUMN %I DROP NOT NULL;',
--             rec.table_schema, rec.table_name, rec.column_name
--         );
--     END LOOP;
-- END $$;

-- -- Verify no NOT NULL columns remain
-- SELECT column_name
-- FROM information_schema.columns
-- WHERE table_schema = 'ufc'
--   AND table_name  = 'fights_staging'
--   AND is_nullable = 'NO';

-- -- ----------------------------------------------------------
-- -- 2) Create Staging Table (raw CSV import)
-- -- ----------------------------------------------------------
-- DROP TABLE IF EXISTS ufc.fights_staging;

-- CREATE TABLE ufc.fights_staging (
--   RedFighter                    TEXT,
--   BlueFighter                   TEXT,
--   RedOdds                       INTEGER,
--   BlueOdds                      INTEGER,
--   RedExpectedValue              NUMERIC,
--   BlueExpectedValue             NUMERIC,
--   "Date"                        TEXT,      -- will convert to DATE later
--   "Location"                    TEXT,
--   "Country"                     TEXT,
--   Winner                        TEXT,
--   TitleBout                     BOOLEAN,
--   WeightClass                   TEXT,
--   Gender                        TEXT,
--   NumberOfRounds                INTEGER,

--   BlueCurrentLoseStreak         INTEGER,
--   BlueCurrentWinStreak          INTEGER,
--   BlueDraws                     INTEGER,
--   BlueAvgSigStrLanded           NUMERIC,
--   BlueAvgSigStrPct              NUMERIC,
--   BlueAvgSubAtt                 NUMERIC,
--   BlueAvgTDLanded               NUMERIC,
--   BlueAvgTDPct                  NUMERIC,
--   BlueLongestWinStreak          INTEGER,
--   BlueLosses                    INTEGER,
--   BlueTotalRoundsFought         INTEGER,
--   BlueTotalTitleBouts           INTEGER,
--   BlueWinsByDecisionMajority    INTEGER,
--   BlueWinsByDecisionSplit       INTEGER,
--   BlueWinsByDecisionUnanimous   INTEGER,
--   BlueWinsByKO                  INTEGER,
--   BlueWinsBySubmission          INTEGER,
--   BlueWinsByTKODoctorStoppage   INTEGER,
--   BlueWins                      INTEGER,
--   BlueStance                    TEXT,
--   BlueHeightCms                 NUMERIC,
--   BlueReachCms                  NUMERIC,
--   BlueWeightLbs                 INTEGER,

--   RedCurrentLoseStreak          INTEGER,
--   RedCurrentWinStreak           INTEGER,
--   RedDraws                      INTEGER,
--   RedAvgSigStrLanded            NUMERIC,
--   RedAvgSigStrPct               NUMERIC,
--   RedAvgSubAtt                  NUMERIC,
--   RedAvgTDLanded                NUMERIC,
--   RedAvgTDPct                   NUMERIC,
--   RedLongestWinStreak           INTEGER,
--   RedLosses                     INTEGER,
--   RedTotalRoundsFought          INTEGER,
--   RedTotalTitleBouts            INTEGER,
--   RedWinsByDecisionMajority     INTEGER,
--   RedWinsByDecisionSplit        INTEGER,
--   RedWinsByDecisionUnanimous    INTEGER,
--   RedWinsByKO                   INTEGER,
--   RedWinsBySubmission           INTEGER,
--   RedWinsByTKODoctorStoppage    INTEGER,
--   RedWins                       INTEGER,
--   RedStance                     TEXT,
--   RedHeightCms                  NUMERIC,
--   RedReachCms                   NUMERIC,
--   RedWeightLbs                  INTEGER,
--   RedAge                        INTEGER,
--   BlueAge                       INTEGER,

--   LoseStreakDif                 INTEGER,
--   WinStreakDif                  INTEGER,
--   LongestWinStreakDif           INTEGER,
--   WinDif                        INTEGER,
--   LossDif                       INTEGER,
--   TotalRoundDif                 INTEGER,
--   TotalTitleBoutDif             INTEGER,
--   KODif                         INTEGER,
--   SubDif                        INTEGER,
--   HeightDif                     NUMERIC,
--   ReachDif                      INTEGER,
--   AgeDif                        INTEGER,
--   SigStrDif                     NUMERIC,
--   AvgSubAttDif                  NUMERIC,
--   AvgTDDif                      NUMERIC,

--   EmptyArena                    TEXT,
--   BMatchWCRank                  INTEGER,
--   RMatchWCRank                  INTEGER,
--   RWFlyweightRank               INTEGER,
--   RWFeatherweightRank           INTEGER,
--   RWStrawweightRank             INTEGER,
--   RWBantamweightRank            INTEGER,
--   RHeavyweightRank              INTEGER,
--   RLightHeavyweightRank         INTEGER,
--   RMiddleweightRank             INTEGER,
--   RWelterweightRank             INTEGER,
--   RLightweightRank              INTEGER,
--   RFeatherweightRank            INTEGER,
--   RBantamweightRank             INTEGER,
--   RFlyweightRank                INTEGER,
--   RPFPRank                      INTEGER,
--   BWFlyweightRank               INTEGER,
--   BWFeatherweightRank           INTEGER,
--   BWStrawweightRank             INTEGER,
--   BWBantamweightRank            INTEGER,
--   BHeavyweightRank              INTEGER,
--   BLightHeavyweightRank         INTEGER,
--   BMiddleweightRank             INTEGER,
--   BWelterweightRank             INTEGER,
--   BLightweightRank              INTEGER,
--   BFeatherweightRank            INTEGER,
--   BBantamweightRank             INTEGER,
--   BFlyweightRank                INTEGER,
--   BPFPRank                      INTEGER,

--   BetterRank                    TEXT,
--   Finish                        TEXT,
--   FinishDetails                 TEXT,
--   FinishRound                   INTEGER,
--   FinishRoundTime               TEXT,
--   TotalFightTimeSecs            INTEGER,

--   RedDecOdds                    INTEGER,
--   BlueDecOdds                   INTEGER,
--   RSubOdds                      INTEGER,
--   BSubOdds                      INTEGER,
--   RKOOdds                       INTEGER,
--   BKOOdds                       INTEGER
-- );

-- -- ----------------------------------------------------------
-- -- 3) Import CSV file
-- -- ----------------------------------------------------------
-- -- Adjust path for your environment:
-- -- COPY ufc.fights_staging
-- -- FROM '/absolute/path/to/Test.csv'
-- -- WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');

-- -- OR use psql client method:
-- -- \copy ufc.fights_staging FROM 'Test.csv' WITH (FORMAT csv, HEADER true, QUOTE '"', DELIMITER ',');

-- -- ----------------------------------------------------------
-- -- 4) Convert Date format (YYYY/MM/DD → DATE)
-- -- ----------------------------------------------------------
-- ALTER TABLE ufc.fights_staging
--   ALTER COLUMN "Date" TYPE DATE
--   USING to_date("Date", 'YYYY/MM/DD');

-- -- ----------------------------------------------------------
-- -- 5) Create Vector Table (for embeddings + FTS)
-- -- ----------------------------------------------------------
-- DROP TABLE IF EXISTS ufc.fights_vectors CASCADE;

-- CREATE TABLE ufc.fights_vectors (
--     id          BIGSERIAL PRIMARY KEY,
--     raw         JSONB NOT NULL,
--     content     TEXT,
--     embedding   VECTOR(1536),
--     search      TSVECTOR,
--     created_at  TIMESTAMPTZ DEFAULT now()
-- );

-- -- Function to flatten JSON values into one string
-- CREATE OR REPLACE FUNCTION ufc.jsonb_to_text(_json JSONB)
-- RETURNS TEXT AS $$
-- BEGIN
--     RETURN (
--         SELECT string_agg(value, ' ')
--         FROM jsonb_each_text(_json)
--     );
-- END;
-- $$ LANGUAGE plpgsql IMMUTABLE;

-- -- Function to refresh the generated columns (content & search)
-- CREATE OR REPLACE FUNCTION ufc.refresh_fight_vectors()
-- RETURNS void AS $$
-- BEGIN
--     UPDATE ufc.fights_vectors
--     SET 
--         content = ufc.jsonb_to_text(raw),
--         search  = to_tsvector('english', ufc.jsonb_to_text(raw))
--     WHERE content IS NULL OR search IS NULL;
-- END;
-- $$ LANGUAGE plpgsql;

-- -- Optional: run after data is inserted from staging
-- INSERT INTO ufc.fights_vectors (raw)
-- SELECT to_jsonb(s) FROM ufc.fights_staging AS s;

-- -- Populate flattened text and FTS vector
-- SELECT ufc.refresh_fight_vectors();

-- -- ----------------------------------------------------------
-- -- 6) Create Indexes
-- -- ----------------------------------------------------------
-- CREATE INDEX fights_vectors_search_ix
--   ON ufc.fights_vectors
--   USING GIN (search);

-- CREATE INDEX fights_vectors_emb_ix
--   ON ufc.fights_vectors
--   USING ivfflat (embedding vector_cosine_ops)
--   WITH (lists = 100);

-- -- ----------------------------------------------------------
-- -- 7) Populate Vector Table from Staging
-- -- ----------------------------------------------------------
-- INSERT INTO ufc.fights_vectors (raw)
-- SELECT to_jsonb(s) FROM ufc.fights_staging AS s;

-- -- ----------------------------------------------------------
-- -- 8) Example Embedding Updates
-- -- ----------------------------------------------------------
-- -- Single row demo
-- -- UPDATE ufc.fights_vectors
-- -- SET embedding = '[0.123, -0.456, ...]'::vector
-- -- WHERE id = 42;

-- -- Bulk update
-- -- CREATE TEMP TABLE _emb (id BIGINT, emb VECTOR(1536));
-- -- INSERT INTO _emb VALUES (1, '[...]'), (2, '[...]');
-- -- UPDATE ufc.fights_vectors v
-- -- SET embedding = e.emb
-- -- FROM _emb e
-- -- WHERE v.id = e.id;

-- -- After embeddings, build ANN index
-- -- CREATE INDEX fights_vectors_emb_ix
-- --   ON ufc.fights_vectors
-- --   USING ivfflat (embedding vector_cosine_ops)
-- --   WITH (lists = 100);

-- -- ----------------------------------------------------------
-- -- 9) Validation Queries
-- -- ----------------------------------------------------------
-- SELECT count(*) AS total_loaded FROM ufc.fights_vectors;

-- SELECT id, left(content, 100) AS preview
-- FROM ufc.fights_vectors
-- WHERE embedding IS NULL
-- LIMIT 5;

-- SELECT id, ts_rank(search, plainto_tsquery('english', 'Rakhmonov')) AS rank,
--        left(content, 120) AS preview
-- FROM ufc.fights_vectors
-- WHERE search @@ plainto_tsquery('english', 'Rakhmonov')
-- ORDER BY rank DESC
-- LIMIT 10;

-- -- Example vector similarity query (after embeddings)
-- -- SELECT id, 1 - (embedding <=> '[...]'::vector) AS cosine_sim,
-- --        left(content, 120)
-- -- FROM ufc.fights_vectors
-- -- ORDER BY embedding <=> '[...]'::vector
-- -- LIMIT 10;

-- -- ✅ End of SQL Pipeline

-- DO $$
-- BEGIN
--   BEGIN
--     ALTER TABLE ufc.fights_staging
--       ALTER COLUMN "Date" TYPE DATE
--       USING to_date("Date"::text, 'YYYY/MM/DD');
--   EXCEPTION
--     WHEN others THEN
--       RAISE NOTICE 'Skipping conversion; Date is already of type DATE.';
--   END;
-- END $$;

-- Create the main UFC fights table
CREATE TABLE ufc_fights (
    fight_id SERIAL PRIMARY KEY,
    
    -- Fighter Names
    red_fighter VARCHAR(100),
    blue_fighter VARCHAR(100),
    
    -- Betting Odds
    red_odds NUMERIC(10,2),
    blue_odds NUMERIC(10,2),
    red_expected_value NUMERIC(10,4),
    blue_expected_value NUMERIC(10,4),
    
    -- Fight Details
    date DATE,
    location VARCHAR(200),
    country VARCHAR(100),
    winner VARCHAR(100),
    title_bout BOOLEAN,
    weight_class VARCHAR(50),
    gender VARCHAR(20),
    number_of_rounds INTEGER,
    
    -- Blue Fighter Stats
    blue_current_lose_streak INTEGER,
    blue_current_win_streak INTEGER,
    blue_draws INTEGER,
    blue_avg_sig_str_landed NUMERIC(10,2),
    blue_avg_sig_str_pct NUMERIC(10,4),
    blue_avg_sub_att NUMERIC(10,2),
    blue_avg_td_landed NUMERIC(10,2),
    blue_avg_td_pct NUMERIC(10,4),
    blue_longest_win_streak INTEGER,
    blue_losses INTEGER,
    blue_total_rounds_fought INTEGER,
    blue_total_title_bouts INTEGER,
    blue_wins_by_decision_majority INTEGER,
    blue_wins_by_decision_split INTEGER,
    blue_wins_by_decision_unanimous INTEGER,
    blue_wins_by_ko INTEGER,
    blue_wins_by_submission INTEGER,
    blue_wins_by_tko_doctor_stoppage INTEGER,
    blue_wins INTEGER,
    blue_stance VARCHAR(20),
    blue_height_cms NUMERIC(10,2),
    blue_reach_cms NUMERIC(10,2),
    blue_weight_lbs INTEGER,
    blue_age INTEGER,
    
    -- Red Fighter Stats
    red_current_lose_streak INTEGER,
    red_current_win_streak INTEGER,
    red_draws INTEGER,
    red_avg_sig_str_landed NUMERIC(10,2),
    red_avg_sig_str_pct NUMERIC(10,4),
    red_avg_sub_att NUMERIC(10,2),
    red_avg_td_landed NUMERIC(10,2),
    red_avg_td_pct NUMERIC(10,4),
    red_longest_win_streak INTEGER,
    red_losses INTEGER,
    red_total_rounds_fought INTEGER,
    red_total_title_bouts INTEGER,
    red_wins_by_decision_majority INTEGER,
    red_wins_by_decision_split INTEGER,
    red_wins_by_decision_unanimous INTEGER,
    red_wins_by_ko INTEGER,
    red_wins_by_submission INTEGER,
    red_wins_by_tko_doctor_stoppage INTEGER,
    red_wins INTEGER,
    red_stance VARCHAR(20),
    red_height_cms NUMERIC(10,2),
    red_reach_cms NUMERIC(10,2),
    red_weight_lbs INTEGER,
    red_age INTEGER,
    
    -- Differential Stats
    lose_streak_dif INTEGER,
    win_streak_dif INTEGER,
    longest_win_streak_dif INTEGER,
    win_dif INTEGER,
    loss_dif INTEGER,
    total_round_dif INTEGER,
    total_title_bout_dif INTEGER,
    ko_dif INTEGER,
    sub_dif INTEGER,
    height_dif NUMERIC(10,2),
    reach_dif NUMERIC(10,2),
    age_dif INTEGER,
    sig_str_dif NUMERIC(10,2),
    avg_sub_att_dif NUMERIC(10,2),
    avg_td_dif NUMERIC(10,2),
    
    -- Additional Stats
    empty_arena NUMERIC(10,2),
    
    -- Rankings
    b_match_wc_rank NUMERIC(10,2),
    r_match_wc_rank NUMERIC(10,2),
    r_w_flyweight_rank NUMERIC(10,2),
    r_w_featherweight_rank NUMERIC(10,2),
    r_w_strawweight_rank NUMERIC(10,2),
    r_w_bantamweight_rank NUMERIC(10,2),
    r_heavyweight_rank NUMERIC(10,2),
    r_light_heavyweight_rank NUMERIC(10,2),
    r_middleweight_rank NUMERIC(10,2),
    r_welterweight_rank NUMERIC(10,2),
    r_lightweight_rank NUMERIC(10,2),
    r_featherweight_rank NUMERIC(10,2),
    r_bantamweight_rank NUMERIC(10,2),
    r_flyweight_rank NUMERIC(10,2),
    r_pfp_rank NUMERIC(10,2),
    b_w_flyweight_rank NUMERIC(10,2),
    b_w_featherweight_rank NUMERIC(10,2),
    b_w_strawweight_rank NUMERIC(10,2),
    b_w_bantamweight_rank NUMERIC(10,2),
    b_heavyweight_rank NUMERIC(10,2),
    b_light_heavyweight_rank NUMERIC(10,2),
    b_middleweight_rank NUMERIC(10,2),
    b_welterweight_rank NUMERIC(10,2),
    b_lightweight_rank NUMERIC(10,2),
    b_featherweight_rank NUMERIC(10,2),
    b_bantamweight_rank NUMERIC(10,2),
    b_flyweight_rank NUMERIC(10,2),
    b_pfp_rank NUMERIC(10,2),
    better_rank VARCHAR(10),
    
    -- Fight Outcome Details
    finish VARCHAR(50),
    finish_details VARCHAR(200),
    finish_round NUMERIC(10,2),
    finish_round_time VARCHAR(10),
    total_fight_time_secs NUMERIC(10,2),
    
    -- Method Odds
    red_dec_odds NUMERIC(10,2),
    blue_dec_odds NUMERIC(10,2),
    r_sub_odds NUMERIC(10,2),
    b_sub_odds NUMERIC(10,2),
    r_ko_odds NUMERIC(10,2),
    b_ko_odds NUMERIC(10,2)
);

-- Create indexes for common queries
CREATE INDEX idx_date ON ufc_fights(date);
CREATE INDEX idx_red_fighter ON ufc_fights(red_fighter);
CREATE INDEX idx_blue_fighter ON ufc_fights(blue_fighter);
CREATE INDEX idx_weight_class ON ufc_fights(weight_class);
CREATE INDEX idx_winner ON ufc_fights(winner);
CREATE INDEX idx_title_bout ON ufc_fights(title_bout);

-- Optional: Add pgvector extension for vector similarity searches
-- First enable the extension (requires superuser or appropriate permissions):
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Then add a vector column if needed for ML/embeddings:
-- ALTER TABLE ufc_fights ADD COLUMN fight_embedding vector(768);

-- Import the CSV file
COPY ufc_fights(
    red_fighter, blue_fighter, red_odds, blue_odds, red_expected_value, blue_expected_value,
    date, location, country, winner, title_bout, weight_class, gender, number_of_rounds,
    blue_current_lose_streak, blue_current_win_streak, blue_draws, blue_avg_sig_str_landed,
    blue_avg_sig_str_pct, blue_avg_sub_att, blue_avg_td_landed, blue_avg_td_pct,
    blue_longest_win_streak, blue_losses, blue_total_rounds_fought, blue_total_title_bouts,
    blue_wins_by_decision_majority, blue_wins_by_decision_split, blue_wins_by_decision_unanimous,
    blue_wins_by_ko, blue_wins_by_submission, blue_wins_by_tko_doctor_stoppage, blue_wins,
    blue_stance, blue_height_cms, blue_reach_cms, blue_weight_lbs,
    red_current_lose_streak, red_current_win_streak, red_draws, red_avg_sig_str_landed,
    red_avg_sig_str_pct, red_avg_sub_att, red_avg_td_landed, red_avg_td_pct,
    red_longest_win_streak, red_losses, red_total_rounds_fought, red_total_title_bouts,
    red_wins_by_decision_majority, red_wins_by_decision_split, red_wins_by_decision_unanimous,
    red_wins_by_ko, red_wins_by_submission, red_wins_by_tko_doctor_stoppage, red_wins,
    red_stance, red_height_cms, red_reach_cms, red_weight_lbs, red_age, blue_age,
    lose_streak_dif, win_streak_dif, longest_win_streak_dif, win_dif, loss_dif,
    total_round_dif, total_title_bout_dif, ko_dif, sub_dif, height_dif, reach_dif,
    age_dif, sig_str_dif, avg_sub_att_dif, avg_td_dif, empty_arena,
    b_match_wc_rank, r_match_wc_rank, r_w_flyweight_rank, r_w_featherweight_rank,
    r_w_strawweight_rank, r_w_bantamweight_rank, r_heavyweight_rank, r_light_heavyweight_rank,
    r_middleweight_rank, r_welterweight_rank, r_lightweight_rank, r_featherweight_rank,
    r_bantamweight_rank, r_flyweight_rank, r_pfp_rank, b_w_flyweight_rank,
    b_w_featherweight_rank, b_w_strawweight_rank, b_w_bantamweight_rank, b_heavyweight_rank,
    b_light_heavyweight_rank, b_middleweight_rank, b_welterweight_rank, b_lightweight_rank,
    b_featherweight_rank, b_bantamweight_rank, b_flyweight_rank, b_pfp_rank, better_rank,
    finish, finish_details, finish_round, finish_round_time, total_fight_time_secs,
    red_dec_odds, blue_dec_odds, r_sub_odds, b_sub_odds, r_ko_odds, b_ko_odds
)
FROM 'C:/path/to/your/ufcmaster.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    NULL '',
    ENCODING 'UTF8'
);
