from paho.mqtt import client as mqtt_client
import random
import time

broker = 'iotfox.ru'
port = 21883
topic = "zigbee2mqtt/light1"

client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected")
        else:
            print("Error on Connection")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"{msg_count}"
        msg_count += 1
        result = client.publish(topic, msg)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


run()
