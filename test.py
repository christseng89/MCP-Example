import csv
import psycopg2

# === 1️⃣ Database connection settings ===
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="n8n",
    user="postgres",
    password="t0210#Chris"
)
cur = conn.cursor()

# === 2️⃣ CSV file path ===
csv_file_path = r"C:\Users\samfi\Downloads\ufc-master.csv"

# === 3️⃣ Target table ===
table_name = "ufc.fights_staging"

# === 4️⃣ Prepare column list (MUST match your table) ===
columns = [
    "RedFighter", "BlueFighter", "RedOdds", "BlueOdds",
    "RedExpectedValue", "BlueExpectedValue", "Date", "Location",
    "Country", "Winner", "TitleBout", "WeightClass", "Gender",
    "NumberOfRounds",

    "BlueCurrentLoseStreak", "BlueCurrentWinStreak", "BlueDraws",
    "BlueAvgSigStrLanded", "BlueAvgSigStrPct", "BlueAvgSubAtt",
    "BlueAvgTDLanded", "BlueAvgTDPct", "BlueLongestWinStreak",
    "BlueLosses", "BlueTotalRoundsFought", "BlueTotalTitleBouts",
    "BlueWinsByDecisionMajority", "BlueWinsByDecisionSplit",
    "BlueWinsByDecisionUnanimous", "BlueWinsByKO", "BlueWinsBySubmission",
    "BlueWinsByTKODoctorStoppage", "BlueWins", "BlueStance",
    "BlueHeightCms", "BlueReachCms", "BlueWeightLbs",

    "RedCurrentLoseStreak", "RedCurrentWinStreak", "RedDraws",
    "RedAvgSigStrLanded", "RedAvgSigStrPct", "RedAvgSubAtt",
    "RedAvgTDLanded", "RedAvgTDPct", "RedLongestWinStreak",
    "RedLosses", "RedTotalRoundsFought", "RedTotalTitleBouts",
    "RedWinsByDecisionMajority", "RedWinsByDecisionSplit",
    "RedWinsByDecisionUnanimous", "RedWinsByKO", "RedWinsBySubmission",
    "RedWinsByTKODoctorStoppage", "RedWins", "RedStance",
    "RedHeightCms", "RedReachCms", "RedWeightLbs",
    "RedAge", "BlueAge",

    "LoseStreakDif", "WinStreakDif", "LongestWinStreakDif",
    "WinDif", "LossDif", "TotalRoundDif", "TotalTitleBoutDif",
    "KODif", "SubDif", "HeightDif", "ReachDif", "AgeDif",
    "SigStrDif", "AvgSubAttDif", "AvgTDDif",

    "EmptyArena", "BMatchWCRank", "RMatchWCRank",
    "RWFlyweightRank", "RWFeatherweightRank", "RWStrawweightRank",
    "RWBantamweightRank", "RHeavyweightRank", "RLightHeavyweightRank",
    "RMiddleweightRank", "RWelterweightRank", "RLightweightRank",
    "RFeatherweightRank", "RBantamweightRank", "RFlyweightRank",
    "RPFPRank", "BWFlyweightRank", "BWFeatherweightRank",
    "BWStrawweightRank", "BWBantamweightRank", "BHeavyweightRank",
    "BLightHeavyweightRank", "BMiddleweightRank", "BWelterweightRank",
    "BLightweightRank", "BFeatherweightRank", "BBantamweightRank",
    "BFlyweightRank", "BPFPRank",

    "BetterRank", "Finish", "FinishDetails", "FinishRound",
    "FinishRoundTime", "TotalFightTimeSecs",

    "RedDecOdds", "BlueDecOdds", "RSubOdds", "BSubOdds",
    "RKOOdds", "BKOOdds"
]


# === 5️⃣ Generate parameterized SQL ===
insert_query = f"""
INSERT INTO {table_name} ({', '.join(columns)})
VALUES ({', '.join(['%s'] * len(columns))})
"""

# === 6️⃣ Read and insert CSV data ===
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    row_count = 0
    for row in reader:
        try:
            # Extract only the columns defined
            values = [row.get(col, None) for col in columns]

            # Execute insert
            cur.execute(insert_query, values)
            row_count += 1

            # Commit every 100 rows (for safety)
            if row_count % 100 == 0:
                conn.commit()
                print(f"Inserted {row_count} rows...")

        except Exception as e:
            print(f"⚠️ Error on row {row_count + 1}: {e}")
            conn.rollback()

# === 7️⃣ Final commit and cleanup ===
conn.commit()
cur.close()
conn.close()
print("✅ Data import completed successfully!")
