import json
import random, requests

import paho.mqtt.client, time
from main import CrudPaciente

host = 'broker.hivemq.com'
port = 1883
topic = "pbl2"
api = CrudPaciente()
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> paho.mqtt.client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = paho.mqtt.client.Client(client_id)
    client.on_connect = on_connect
    client.connect(host, port)
    return client


def subscribe(client:paho.mqtt.client):
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        print(f"Recebeu`{msg.payload.decode()}` from `{msg.topic}` topic")
        requests.post(url=f'https://connect-covid.herokuapp.com/patient', json=data)



    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()