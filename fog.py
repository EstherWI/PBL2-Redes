import json
import random, time,threading

import paho.mqtt.client



host = 'localhost'
port = 1883
topic = "paciente_pbl"
topic2 = "paciente_broker"
lista = []


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

def connect_broker() -> paho.mqtt.client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to HiveMQ!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = paho.mqtt.client.Client(client_id)
    client.on_connect = on_connect
    client.connect('broker.hivemq.com', port)
    return client


def subscribe(client: paho.mqtt.client, client_broker: paho.mqtt.client):
    def on_message(client, userdata, message)->list:
        lista.append(str(message.payload.decode("utf-8")))
        time.sleep(1.5)
        client_broker.publish(topic2, str(lista))
        #print("received message =",str(message.payload.decode("utf-8")))
    client.subscribe(topic)
    client.on_message = on_message




def run():
    client = connect_mqtt()
    client_broker = connect_broker()
    subscribe(client,client_broker)
    client.loop_forever()


if __name__ == '__main__':
    run()
