import serial
from paho.mqtt import client as mqtt_client

# to publish "msg" to client "topic"
def publish(client, msg):
  result = client.publish(topic, msg)
  # result: [0, 1]
  status = result[0]
  print(f"Send `{msg}` to topic `{topic}`" if status == 0 else f"Failed to send message to topic {topic}")

########################################
######### Init UART connection #########
port_path = '/dev/ttyAMA0'
# start communication 9600 8N1
ser = serial.Serial(
  port = port_path,\
  baudrate = 9600,\
  parity = serial.PARITY_NONE,\
  stopbits = serial.STOPBITS_ONE,\
  bytesize = serial.EIGHTBITS,\
  timeout = 0)
print("Connected to: " + ser.portstr)

########################################
######### Init MQTT connection #########
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/wireless"
client_id = 'python-mqtt-389'       # generate client ID with pub prefix randomly
username = 'wireless2-midproj'
password = 'wireless2-midpw'

def connect_mqtt():
  def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!" if rc==0 else "Failed to connect, return code "+str(rc))
  client = mqtt_client.Client(client_id)
  client.username_pw_set(username, password)
  client.on_connect = on_connect
  client.connect(broker, port)
  return client

client = connect_mqtt()
client.loop_start()

#################################
######### Main function #########

seq = []  #this will store the line

while True:
  for c in ser.read():
    seq.append(chr(c)) #convert from ANSII
    joined_seq = ''.join(str(v) for v in seq) #Make a string from array

    if chr(c) == '\n':
      # message format: <light_voltage>,<humidity(%)>,<temperature(*C)>,<feels_like(*C)>
      publish(client, joined_seq.strip())
      seq = []
      break

ser.close()