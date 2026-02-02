import pyspark.sql.functions as F
from src.common.schema import schema
from src.common.spark_session import spark_session
from src.common.paths import (
    SILVER_PATH,
    EVENTS_PER_MINUTE,
    CHECKPOINT_EVENTS_PER_MINUTE_PATH
)

def main():
    spark = spark_session("gold_production_events_per_minute")

    read_silver_df = (
        spark
        .readStream
        .format("parquet")
        .schema(schema)
        .load(SILVER_PATH)
    )

    gold_events_per_minute = (
        read_silver_df
        .withWatermark("event_time", "10 minutes")
        .groupBy(
            F.window("event_time", "1 minute")
        )
        .count()
        .select(
            F.col("window.start").alias("minute_start"),
            F.col("window.end").alias("minute_end"),
            F.col("count").alias("event_count")
        )
    )

    query = (
        gold_events_per_minute.writeStream
        .format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", EVENTS_PER_MINUTE)
        .option("checkpointLocation", CHECKPOINT_EVENTS_PER_MINUTE_PATH)
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
    
