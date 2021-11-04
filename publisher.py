import paho.mqtt.client, time, json, random, names
import threading, os

threads = []
result = []
maxNrOfThreads = 10
topic = "paciente_pbl"


# O retorno de chamada para quando uma mensagem publish é recebida do servidor.
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    global result
    while len(result) != maxNrOfThreads:
        r = random.randint(0,100)
        if r not in result:
            result.append(r)
            break
    client=paho.mqtt.client.Client(client_id=str(r),clean_session=False, userdata=names.get_full_name())
    client.on_connect = on_connect
    client.connect(host='localhost', port = 1883)
    return client

def calculaGravidade(data)-> float:
    gravidade = 0
    gravidade += abs(data['temp'] - 36)
    gravidade += abs(data['saturacao'] - 96)
    gravidade += abs(data['freq'] - 70)
    return round(gravidade,2)

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

def worker():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

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