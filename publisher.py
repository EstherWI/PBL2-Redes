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


import paho.mqtt.client, time, json, random, names
import threading, os
from dotenv import load_dotenv

load_dotenv()

#Este arquivo é responsável por realizar a publicação e atualização de X pacientes no broker local.
#Sendo estes pacientes gerados de modo aleatório, em conjunto com seus dados de sinais vitais randomicamente.
#É estabelecido também um cálculo de gravidade de acordo com seus parâmetros de sinais vitais
#para posteriormente na Fog ordená-los de acordo com os N mais graves.


threads = []
result = []
#Quantidade máxima de pacientes criados em uma só execução
maxNrOfThreads = 15
topic = "paciente_pbl"

#Esta função é responsável pela conexão de um cliente no broker público, contando com uma verficação de ID gerado
#em um determinado intervalo randomico,para não haver conflito entre os clientes do publisher e subscriber.
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    global result
    while len(result) != maxNrOfThreads:
        r = random.randint(int(os.getenv("A")),int(os.getenv("B")))
        if r not in result:
            result.append(r)
            break
    client=paho.mqtt.client.Client(client_id=str(r),clean_session=False, userdata=names.get_full_name())
    client.on_connect = on_connect
    client.connect(host='localhost', port = 1883)
    return client

#Função que realiza o cálculo de gravidade do paciente, de acordo com alguns padrões de sinais vitais estabelecidos.
def calculaGravidade(data)-> float:
    gravidade = 0
    gravidade += abs(data['temp'] - 36)
    gravidade += abs(data['saturacao'] - 96)
    gravidade += abs(data['freq'] - 70)
    return round(gravidade,2)

#Função que gera um paciente grave quando escolhida. Sendo os parâmetros graves estabelecidos em determinado intervalo randomico.

def pacienteGrave(contador, fog, name) -> dict:
    data ={
        "nome": name,
        "id": contador,
        "saturacao":random.randint(0, 95),
        "temp":round(random.uniform(37.5, 42), 1),
        "freq":random.randint(100,140),
        "pressao1":random.randint(140,220),
        "pressao2":random.randint(85,100),
        "status":0,
        "fog": fog
    }
    data['status'] = calculaGravidade(data)
    return data

#Função que gera um paciente leve , quando escolhida. Com intervalos de parãmetros já estabelecidos e gerados randomicamente.
def pacienteLeve(contador, fog, name) ->dict:
    data = {
        "nome": name,
        "id":contador,
        "saturacao":random.randint(96, 100),
        "temp":round(random.uniform(35.5, 37.4), 1),
        "freq":random.randint(60,99),
        "pressao1":random.randint(110,130),
        "pressao2":random.randint(70,84),
        "status":0,
        "fog":fog
    }
    data['status'] = calculaGravidade(data)
    return data

#Função responsável por escolher de maneira randomica o tipo de paciente a ser gerado(grave ou leve)
#com um time de 3 segundos . E publica no broker local, para a Fog obtê-los.
def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        choice = random.randint(0,1)
        if choice == 0:
            msg = pacienteGrave(int(client._client_id), "", client._userdata)
        else:
            msg = pacienteLeve(int(client._client_id), "", client._userdata)

        result = client.publish(topic, json.dumps(msg))

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

#inicializa a conexão do cliente publisher
def worker():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

#Thread responsável pela geração de um número X de pacientes a cada execução do arquivo publisher.py
def main():
    for _ in range(maxNrOfThreads):
        thr = threading.Thread(target=worker)
        threads.append(thr)
        thr.setDaemon(True)
        thr.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()