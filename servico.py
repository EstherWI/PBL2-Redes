import json
import random
import requests
import paho.mqtt.client


host = 'broker.hivemq.com'
port = 1883
topic = "paciente_broker"

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


def subscribe(client: paho.mqtt.client):
    def on_message(client, userdata, msg):
        data = eval(json.loads(json.dumps(str(msg.payload.decode("utf-8")))))
        ordenada = sorted(data, key=lambda k: k['status'], reverse=True) 
        requests.post(url=f'https://connect-covid.herokuapp.com/patients', json=ordenada)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
