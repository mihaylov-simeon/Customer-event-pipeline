from src.common.schema import schema
from src.common.spark_session import spark_session
from src.common.paths import (
    DATA_PATH,
    BRONZE_PATH,
    BRONZE_CHECKPOINT_PATH
)

def main():
    spark = spark_session("bronze_event_ingestion")

    event_stream = (
        spark.readStream
        .schema(schema)
        .json(DATA_PATH)
    )

    query = (
        event_stream.writeStream
            .format("parquet")
            .outputMode("append")
            .trigger(processingTime="10 seconds")
            .option("path", BRONZE_PATH)
            .option("checkpointLocation", BRONZE_CHECKPOINT_PATH)
            .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
