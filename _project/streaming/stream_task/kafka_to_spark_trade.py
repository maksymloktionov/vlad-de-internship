# Databricks notebook source
import pyspark.sql.functions as f
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark.conf.set("spark.sql.caseSensitive", "true")

# COMMAND ----------

# MAGIC %run ./get_confluent_config

# COMMAND ----------

server = confluent_config['bootstrap.servers']
topic = "crypto"

# COMMAND ----------

kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", server) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 100) \
    .load()

json_schema = StructType([
    StructField("e", StringType(), True),
    StructField("E", StringType(), True),
    StructField("s", StringType(), True),
    StructField("t", StringType(), True),
    StructField("p", StringType(), True),
    StructField("q", StringType(), True),
    StructField("T", StringType(), True),
    StructField("m", StringType(), True),
    StructField("M", StringType(), True),
])

kafka_stream_df = kafka_stream.selectExpr("timestamp", "CAST(value AS STRING)")
kafka_stream_df = kafka_stream_df \
    .withColumn("json", f.from_json(f.col("value"), json_schema)) \
    .select(
        f.col("timestamp"),
        f.col("json.*")
    ) \
    .select(
        f.col("timestamp"),
        f.col("e").alias("event"),
        f.col("E").alias("event_time_unix"),
        f.col("s").alias("symbol"),
        f.col("t").alias("trade_id"),
        f.col("p").alias("price"),
        f.col("q").alias("quantity"),
        f.col("T").alias("trade_time"),
        f.col("m").alias("is_market_maker"),
        f.col("M").alias("ignore")
    )

kafka_stream_df.printSchema()

kafka_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/crypto/last_checkpoint") \
    .trigger(processingTime='30 seconds') \
    .option("spark.sql.shuffle.partitions", "2") \
    .toTable("crypto.default.orders_new")
