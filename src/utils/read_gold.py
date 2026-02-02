import sys
from pathlib import Path

# Project root fixer
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
from src.common.spark_session import spark_session
from src.common.paths import (
    ACTIVE_USERS,
    EVENTS_PER_MINUTE,
    MOST_PURCHASES_PER_DEVICE,
    REVENUE_PER_WINDOW
)

def main():
    spark = spark_session("silver_event_transformation")

    spark.sparkContext.setLogLevel("WARN")

    print("\n=== Active users per window ===")
    spark.read.parquet(ACTIVE_USERS).show(truncate=False)

    print("\n=== Events per minute ===")
    spark.read.parquet(EVENTS_PER_MINUTE).show(truncate=False)

    print("\n=== Most purchases per device ===")
    spark.read.parquet(MOST_PURCHASES_PER_DEVICE).show(truncate=False)

    print("\n=== Revenue per window ===")
    spark.read.parquet(REVENUE_PER_WINDOW).show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()