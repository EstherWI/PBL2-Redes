'''
 * Componente Curricular: Módulo Integrado de Concorrência e Conectividade
 * Autor: Gustavo dos Santos Menezes Alves e Esther de Santana Araújo
 * Data: 4/11/2021
 *
 * Declaro que este código foi elaborado por nós de forma colaborativa e
 * não contém nenhum trecho de código de outro colega ou de outro autor,
 * tais como provindos de livros e apostilas, e páginas ou documentos
 * eletrônicos da Internet. Qualquer trecho de código de outra autoria que
 * uma citação para o  não a minha está destacado com  autor e a fonte do
 * código, e estou ciente que estes trechos não serão considerados para fins
 * de avaliação. Alguns trechos do código podem coincidir com de outros
 * colegas pois estes foram discutidos em sessões tutorias.
 '''

import json, os
import requests
import paho.mqtt.client
from dotenv import load_dotenv

load_dotenv()


host = 'localhost'
port = 1883
topic = "paciente_pbl"
topic2 = "paciente_broker"
lista = []
ordenada = []
paciente = None
heroku = 'https://connect-covid.herokuapp.com'


def connect_mqtt() -> paho.mqtt.client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = paho.mqtt.client.Client(client_id=f'python-mqtt-{601}', clean_session=False)
    client.on_connect = on_connect
    client.connect(host, port)
    return client

def connect_broker() -> paho.mqtt.client:
    def on_connect_broker(client, userdata, flags, rc):
        if rc == 0:
            print("Connecto ao HiveMQ!")
        else:
            print("Falha na conexão, return code %d\n", rc)

    client = paho.mqtt.client.Client(client_id=f'python-mqtt-{600}',clean_session=False)
    client.on_connect = on_connect_broker
    client.connect('broker.hivemq.com', port)
    return client


def subscribe(client: paho.mqtt.client, client_broker: paho.mqtt.client):
    def on_message(client, userdata, message)->list:
        data = json.loads(str(message.payload.decode("utf-8")))
        print(data)
        idSelect = requests.get(url=f'{heroku}/getId').json()
        n = requests.get(url=f'{heroku}/getN').json()
        data['fog'] = os.getenv("FOG")
        index = next((i for i, item in enumerate(lista) if item['id'] == data['id']), -1) 
        if index != -1:
            lista[index] = data
        else:
            lista.append(data)
        index = next((i for i, item in enumerate(lista) if item['id'] == idSelect), -1) 
        if index != -1:
            resultado = client_broker.publish("MonitorarPaciente",str(lista[index]))
            print(str(lista[index]))
            status = resultado[0]
            if status == 0:
                print(f"Foi enviado com sucesso para topico de monitorar")
            else:
                print(f"Falhou ao enviar a mensagem ao topico de monitorar")
        ordenada = sorted(lista, key=lambda k: k['status'], reverse=True) 
        result = client_broker.publish(topic2, str(ordenada[0:n]))
        status = result[0]
        if status != 0:
            print(f"Falhou ao enviar a mensagem ao topico {topic2}")
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client_broker = connect_broker()
    subscribe(client,client_broker)
    client.loop_forever()


if __name__ == '__main__':
    run()