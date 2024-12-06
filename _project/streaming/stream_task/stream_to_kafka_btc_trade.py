# Databricks notebook source
# MAGIC %pip install --upgrade six confluent_kafka

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from websocket import WebSocketApp
import json
from confluent_kafka import Producer

# COMMAND ----------

# MAGIC %run ./get_confluent_config

# COMMAND ----------

# My kafka config
# kafka_config = {
#     'bootstrap.servers': '35.181.52.4:9092',
#     'client.id': 'websocket-producer'
# }

topic = "crypto"

producer = Producer(confluent_config)

def delivery_report(err, msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

def on_message(ws, message):
    data = json.loads(message)
    producer.produce(topic, key=None, value=json.dumps(data), callback=delivery_report)
    producer.flush()

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed:", close_msg)

def on_open(ws):
    print("WebSocket connection opened!")

if __name__ == "__main__":
    url = f"wss://stream.binance.com:443/ws/btcusdt@trade"
    
    ws = WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    ws.run_forever()

