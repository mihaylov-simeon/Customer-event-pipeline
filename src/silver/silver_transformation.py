from src.common.schema import schema
from src.common.spark_session import spark_session
from src.common.paths import (
    BRONZE_PATH,
    SILVER_PATH,
    SILVER_CHECKPOINT_PATH
)

def main():
    spark = spark_session("silver_event_transformation")

    spark.sparkContext.setLogLevel("WARN")

    read_bronze_df = (
        spark
        .readStream
        .format("parquet")
        .schema(schema)
        .option("maxFilesPerTrigger", 20)
        .load(BRONZE_PATH)
        )

    silver_final = (
        read_bronze_df
        .withWatermark("event_time", "10 minutes")
        .dropDuplicates(["event_id"])
    )

    query = (
        silver_final.writeStream
        .format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", SILVER_PATH)
        .option("checkpointLocation", SILVER_CHECKPOINT_PATH)
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
