import pyspark.sql.functions as F
from src.common.schema import schema
from src.common.spark_session import spark_session
from src.common.paths import (
    SILVER_PATH,
    REVENUE_PER_WINDOW,
    CHECKPOINT_REVENUE_PER_WINDOW
)

def main():
    spark = spark_session("gold_production_revenue_per_window")

    read_silver_df = (
        spark
        .readStream
        .format("parquet")
        .schema(schema)
        .load(SILVER_PATH)
    )

    gold_revenue_per_window = (
        read_silver_df
        .withWatermark("event_time", "10 minutes")
        .filter(
            F.col("event_type") == "purchase"
        )
        .groupBy(
            F.window("event_time", "5 minutes")
        )
        .agg(
            F.sum("event_value").alias("revenue")
        )
        .select(
            F.col("window.start").alias("minute_start"),
            F.col("window.end").alias("minute_end"),
            F.col("revenue")
        )
    )

    query = (
        gold_revenue_per_window.writeStream
        .format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", REVENUE_PER_WINDOW)
        .option("checkpointLocation", CHECKPOINT_REVENUE_PER_WINDOW)
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
    
