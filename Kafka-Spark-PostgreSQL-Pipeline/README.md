# Steps to Run the Pipeline

1. Run the `RpiMQTT.py` script in Raspberry Pi to collect the data and publish to MQTT.

2. Run the `MQTT_Kafka.py` script to publish the data from MQTT to kafka servers.

3. Run the `SparkStreaming.py` script to get the data from Kafka through Spark and store it in PostgreSQL.
