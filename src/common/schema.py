import pyspark.sql.types as T

schema = T.StructType([
    T.StructField("event_id", T.StringType(), nullable=False),
    T.StructField("user_id", T.StringType(), nullable=False),
    T.StructField("event_time", T.TimestampType(), nullable=False),
    T.StructField("event_type", T.StringType(), nullable=False),
    T.StructField("device_type", T.StringType(), nullable=True),
    T.StructField("event_value", T.DecimalType(10, 2), nullable=True)
])