from paho.mqtt import client as mqtt_client
import random
import json

# mqtt settings
broker = 'iotfox.ru'
port = 21883

# topics settings
topics = dict()
topics["zigbee2mqtt/temp"] = "room1"
topics["zigbee2mqtt/light1"] = "room1"
topics["zigbee2mqtt/light2"] = "room2"
topics["zigbee2mqtt/contact"] = "room2"

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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"{msg.payload.decode()} {msg.topic}")
        json_ = msg.payload.decode()
        topic = topics.get(msg.topic)
        if topic is not None:
            data = json.loads(json_)
            if not isinstance(data, str):
                for key in data:
                    client.publish(str("home/" + str(topics.get(msg.topic)) + '/' + str(key)), str(data.get(key)))
            else:
                client.publish(str(topic), msg.payload.decode())

    client.subscribe("zigbee2mqtt/#")
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


run()
