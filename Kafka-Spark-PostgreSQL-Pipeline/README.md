![Kafka-Spark](https://user-images.githubusercontent.com/35187384/108131388-7aff3500-70b1-11eb-8113-9d3ef66a8da6.jpg)

This project is about streaming real-time sensor data through MQTT protocol. Apache Kafka then used to process the data with Spark and upload it in PostgreSQL Database.

# Steps to Run the Pipeline

1. Run the `RpiMQTT.py` script in Raspberry Pi to collect the data and publish to MQTT.

2. Run the `MQTT_Kafka.py` script to publish the data from MQTT to kafka servers.

3. Run the `SparkStreaming.py` script to get the data from Kafka through Spark and store it in PostgreSQL.
