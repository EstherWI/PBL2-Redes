import paho.mqtt.client, time

topic = "pbl2"

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

    client=paho.mqtt.client.Client(client_id='Esther',clean_session=False)
    client.on_connect = on_connect
    client.connect(host='broker.hivemq.com', port = 1883)
    return client

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = [{"Yan": 12345678, "Pedro":99999999, "Ana": 8765}]
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def main():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    main()