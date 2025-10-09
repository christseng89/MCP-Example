import csv
import psycopg2
from datetime import datetime

# === 1) DB connection ===
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="n8n",
    user="postgres",
    password="tnnnn#Xxxxx"
)
cur = conn.cursor()

# Ensure we are in the right schema
cur.execute("SET search_path TO public;")

# === 2) CSV path ===
csv_file_path = r"C:\Users\samfi\Downloads\ufc-master.csv"

# === 3) Target table (FIXED: was 'ufc-master', should be 'ufc_master') ===
table_name = 'ufc_master'

# === 4) Column list (must match the table) ===
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

# Build the INSERT statement (no quotes needed if using lowercase table name)
placeholders = ", ".join(["%s"] * len(columns))
insert_sql = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'


def clean_value(val, col_name):
    """Convert empty strings to None, handle special cases"""
    if val is None or (isinstance(val, str) and val.strip() == ""):
        return None

    # Handle boolean column
    if col_name == "TitleBout":
        if isinstance(val, str):
            v = val.strip().lower()
            if v in ("true", "t", "1", "yes"):
                return True
            elif v in ("false", "f", "0", "no"):
                return False
        return None

    # Keep strings as-is
    if isinstance(val, str):
        return val.strip()

    return val


# === 5) Import data ===
batch_count = 0
error_count = 0
error_rows = []

try:
    with open(csv_file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):
            try:
                vals = []
                for col in columns:
                    raw_val = row.get(col, None)
                    cleaned_val = clean_value(raw_val, col)
                    vals.append(cleaned_val)

                cur.execute(insert_sql, vals)
                batch_count += 1

                # Commit in batches for better performance
                if batch_count % 500 == 0:
                    conn.commit()
                    print(f"✓ Committed {batch_count} rows...")

            except Exception as e:
                error_count += 1
                error_msg = f"Row {i}: {str(e)}"
                error_rows.append(error_msg)
                print(f"⚠️ {error_msg}")

                # Show first few values for debugging
                if error_count <= 5:
                    print(
                        f"   Data: {row.get('RedFighter', 'N/A')} vs {row.get('BlueFighter', 'N/A')}")

                conn.rollback()

                # Stop after too many errors
                if error_count > 100:
                    print("❌ Too many errors. Stopping import.")
                    break

    # Final commit
    conn.commit()

    # Summary
    print("\n" + "="*60)
    print(f"✅ Import completed!")
    print(f"   Successfully inserted: {batch_count} rows")
    print(f"   Errors: {error_count} rows")
    if error_rows:
        print(f"\nFirst errors:")
        for err in error_rows[:10]:
            print(f"   {err}")
    print("="*60)

except Exception as e:
    print(f"❌ Fatal error: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()
    print("\n🔌 Database connection closed.")
