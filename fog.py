import json
import random, time
import paho.mqtt.client
from main import CrudPaciente
from pub import Pub

host = 'localhost'
port = 1883
topic = "paciente_pbl"
api = CrudPaciente()
lista = [] 
ordenada = []
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
    def on_message(client, userdata, msg):
        lista.append(str(msg.payload.decode("utf-8")))
        print(f"Received `{msg}` from `{msg.topic}` topic")
        #publish(client_broker, lista)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    #client_broker = connect_broker()
    subscribe(client)
    #pub = Pub()
    client.loop_forever()


if __name__ == '__main__':
    run()
