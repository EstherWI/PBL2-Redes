import paho.mqtt.client, os, urllib

# Retorno de chamada quando o cliente recebe uma resposta de conexão com o servidor
def on_connect(client,userdata, flags, rc):
    print("Conectado: "+ str(client._client_id))
    print("rc: " + str(rc))
    client.subscribe(topic="teste", qos=2)

# O retorno de chamada para quando uma mensagem publish é recebida do servidor.
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = paho.mqtt.client.Client(client_id='esther', clean_session=False)

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Connect
mqttc.connect(host='broker.hivemq.com', port = 1883)
mqttc.publish("pbl2", 'string')


# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))