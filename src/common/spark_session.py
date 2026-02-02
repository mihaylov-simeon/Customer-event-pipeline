from pyspark.sql import SparkSession

def spark_session(app_name: str) -> SparkSession:
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.hadoop.fs.defaultFS", "file:///")
        .config("spark.hadoop.fs.viewfs.impl", "org.apache.hadoop.fs.LocalFileSystem")
        .config("spark.hadoop.fs.AbstractFileSystem.viewfs.impl", "org.apache.hadoop.fs.local.LocalFs")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark