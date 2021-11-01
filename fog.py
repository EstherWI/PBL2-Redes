import json
import random
import paho.mqtt.client

host = 'localhost'
port = 1883
topic = "paciente_pbl"
topic2 = "paciente_broker"
lista = []
ordenada = []
n = 10
fogs = 0

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

    client = paho.mqtt.client.Client(client_id,clean_session=False, userdata="fog1")
    client.on_connect = on_connect
    client.connect('broker.hivemq.com', port)
    return client


def subscribe(client: paho.mqtt.client, client_broker: paho.mqtt.client):
    def on_message(client, userdata, message)->list:
        data = json.loads(str(message.payload.decode("utf-8")))
        index = next((i for i, item in enumerate(lista) if item['id'] == data['id']), -1) 
        if index != -1:
            lista[index] = data
        else:
            lista.append(data)
        ordenada = sorted(lista, key=lambda k: k['status'], reverse=True) 
        client_broker.publish(topic2, str(ordenada[0:n]))
        print("received message =",str(message.payload.decode("utf-8")))
    def on_message_HIVE(client, userdata, message)->list:
        global n
        n = str(message.payload.decode("utf-8"))
    def on_message_FOGS(client, userdata, message)->list:
        global fogs
        fogs = str(message.payload.decode("utf-8"))
    client.subscribe("/Fogs")
    client.on_message = on_message_FOGS
    client.subscribe(topic)
    client.on_message = on_message
    client_broker.subscribe("/N")
    client_broker.on_message = on_message_HIVE


def run():
    client = connect_mqtt()
    client_broker = connect_broker()
    client_broker.publish("/Fogs", fogs+1)
    subscribe(client,client_broker)
    client.loop_forever()

if __name__ == '__main__':
    run()
