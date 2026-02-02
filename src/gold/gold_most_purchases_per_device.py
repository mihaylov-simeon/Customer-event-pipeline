import pyspark.sql.functions as F
from src.common.schema import schema
from src.common.spark_session import spark_session
from src.common.paths import (
    SILVER_PATH,
    MOST_PURCHASES_PER_DEVICE,
    CHECKPOINT_MOST_PURCHASES_PER_DEVICE
)

def main():
    spark = spark_session("gold_production_most_purchases_per_device")

    read_silver_df = (
        spark
        .readStream
        .format("parquet")
        .schema(schema)
        .load(SILVER_PATH)
    )

    gold_most_purchases_per_device = (
        read_silver_df
        .withWatermark("event_time", "10 minutes")
        .filter(
            F.col("event_type") == "purchase"
        )
        .groupBy(
            F.window("event_time", "5 minutes"),
            F.col("device_type")
        )
        .agg(
            F.sum("event_value").alias("revenue_per_device"),
            F.count("*").alias("purchase_count")
        )
        .select(
            F.col("window.start").alias("minute_start"),
            F.col("window.end").alias("minute_end"),
            F.col("device_type"),
            F.col("revenue_per_device"),
            F.col("purchase_count")
        )
    )

    query = (
        gold_most_purchases_per_device.writeStream
        .format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", MOST_PURCHASES_PER_DEVICE)
        .option("checkpointLocation", CHECKPOINT_MOST_PURCHASES_PER_DEVICE)
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
    
