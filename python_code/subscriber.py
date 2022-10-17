# python3.6

import random

from paho.mqtt import client as mqtt_client
from functions import *


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/wireless"
# generate client ID with pub prefix randomly
client_id = 'python-mqtt-test-sub'
username = 'wireless2-midproj-sub'
password = 'wireless2-midpw-sub'

PERIOD = 60
cnt = 0
sensor_data_list = [0,0,0,0]

def connect_mqtt() -> mqtt_client:
  def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

  client = mqtt_client.Client(client_id)
  client.username_pw_set(username, password)
  client.on_connect = on_connect
  client.connect(broker, port)
  return client


def subscribe(client: mqtt_client):

  def on_message(client, userdata, msg):
    try:
      global cnt
      global sensor_data_list
      decoded_data = msg.payload.decode()
      print(f"Received `{decoded_data}` from `{msg.topic}` topic")
      raw_data = [float(e) for e in decoded_data.strip().split(',')]

      for i in range(len(raw_data)):
        sensor_data_list[i] += float(raw_data[i])

      cnt += 1

      if cnt == PERIOD:
        con_session = connect_to_postgresql()
        insert_to_sensor_data_table(sensor_data_list, PERIOD, con_session)
        sensor_data_list = [0,0,0,0]
        cnt = 0
        disconnect_from_postgresql(con_session)

    except Exception as e:
      print("Error has occured.", e)

  client.subscribe(topic)
  client.on_message = on_message


def run():
  client = connect_mqtt()
  subscribe(client)
  client.loop_forever()


if __name__ == '__main__':
  run()