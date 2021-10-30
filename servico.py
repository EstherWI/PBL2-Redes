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
        print(msg.payload.decode("utf-8"))
        data = json.loads(str(msg.payload.decode("utf-8")))
        if data['method'] == "post":
            requests.post(
                url=f'https://connect-covid.herokuapp.com/patient', json=data)
        else:
            requests.put(
                url=f'https://connect-covid.herokuapp.com/patient/' + str(data['id']), json=data)
        print(f"Recebeu`{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
