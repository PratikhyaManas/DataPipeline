import sys
import datetime
import json
import paho.mqtt.client as mqtt
import random
import time

mqtt_hostname = "localhost"
mqtt_queue = "RpiValue"

while True:
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = round(random.uniform(20.0, 32.0), 2)
    humidity = round(random.uniform(60.0, 72.0), 2)
    pressure = round(random.uniform(100.0, 125.0), 2)
    waterLevel = round(random.uniform(40.0, 60.0), 2)
    if humidity is not None and temperature is not None:
        # body = str(dt) + ",RaspberryPi-4," + str(temperature) + "," + str(humidity) + "," +str(pressure) + "," + str(waterLevel)
        body = "%s,RaspberryPi-4,%s,%s,%s,%s" % (dt, temperature, humidity, pressure, waterLevel)
        print("body \n", body)
        # Publisher
        client = mqtt.Client()
        client.connect(mqtt_hostname, 1883, 60)
        client.publish(mqtt_queue, str(body))
        client.disconnect()
        time.sleep(15)

    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
