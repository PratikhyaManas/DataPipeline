import os
import time
from kafka import KafkaProducer
import paho.mqtt.client as mqtt
from json import dumps
from kafka.errors import KafkaError, NoBrokersAvailable
topic_mqtt = "RpiValue"
topic_kafka = "RpiValueKafka"

def send_message_to_kafka(message):
    print(str(message).replace("\"", ""))
    print("sending message to kafka: %s" % message)
    producer.send(topic_kafka, message)


def mqtt_to_kafka_run():
    print("MQTT To Kafka")
    client = mqtt.Client()
    
    on_connect = lambda client, userdata, flags, rc: client.subscribe(topic_mqtt)
    client.on_connect = on_connect
    
    on_message = lambda client, userdata, msg: send_message_to_kafka(msg.payload.decode())
    client.on_message = on_message
    
    on_disconnect = lambda client, user_data, rc: print("""Disconnected client: %s user_data: %s rc:%s """ % (client, user_data, rc))
    client.on_disconnect = on_disconnect
    
    client.connect('192.168.0.104', 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    attempts = 0
    while attempts < 10:
        try:
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
            mqtt_to_kafka_run()
        except NoBrokersAvailable:
            print("No Brokers. Attempt %s" % attempts)
            attempts = attempts + 1
            time.sleep(2)