# Databricks notebook source
def read_config():
  config = {}
  with open("client2.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config

confluent_config = read_config()

print(confluent_config)
