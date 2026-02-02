import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pyspark.sql.functions as F
from src.common.schema import schema
from src.common.spark_session import spark_session
from src.common.paths import (
    SILVER_PATH,
    ACTIVE_USERS,
    CHECKPOINT_ACTIVE_USERS_PER_WINDOW
)

def main():
    spark = spark_session("gold_production_active_users_per_window")

    read_silver_df = (
        spark
        .readStream
        .format("parquet")
        .schema(schema)
        .load(SILVER_PATH)
    )

    gold_active_users_per_window = (
        read_silver_df
        .withWatermark("event_time", "10 minutes")
        .groupBy(
            F.window("event_time", "5 minutes")
        )
        .agg(
            F.approx_count_distinct("user_id").alias("active_users")
        )
        .select(
            F.col("window.start").alias("minute_start"),
            F.col("window.end").alias("minute_end"),
            F.col("active_users")
        )
    )

    query = (
        gold_active_users_per_window.writeStream
        .format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", ACTIVE_USERS)
        .option("checkpointLocation", CHECKPOINT_ACTIVE_USERS_PER_WINDOW)
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
    