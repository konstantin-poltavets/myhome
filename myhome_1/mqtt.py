import sqlite3
from datetime import date, datetime, timezone
import paho.mqtt.client as mqtt
import time
import json
import csv
import pytz

def on_message_msgs(mosq, obj, msg):
    print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.today()
    cursor.execute('''INSERT INTO myhome_1_mqtt(topic, payload, created_date) VALUES (?,?,?)''', (msg.topic, msg.payload, today,))
    conn.commit()
    conn.close
#    time.sleep(60)

def on_message_bytes(mosq, obj, msg):
    print("ZIGBEE" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.now().replace(tzinfo=None)
    cursor.execute('''INSERT INTO myhome_1_mqtt(topic, payload, created_date) VALUES (?,?,?)''', (msg.topic, msg.payload, today,))
    conn.commit()
    conn.close


def on_message_electro(mosq, obj, msg):
    print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    pload = json.loads(msg.payload.decode('utf-8'))
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.now()
    today = today.replace(tzinfo=pytz.timezone("Europe/Kiev"))
    cursor.execute('''INSERT INTO myhome_1_electrometr(param, created_date, measured_time, current, energy, voltage, frequency, pf, power) 
    VALUES (?,?,?,?,?,?,?,?,?)''', ('1', today, str(pload['measured_time']),float(pload['current']),float(pload['energy']),float(pload['voltage']), float(pload['frequency']),float(pload['pf']),float(pload['power'])))
    conn.commit()
    conn.close
    
    
    
def on_message_electro_all(mosq, obj, msg):
    
    values = msg.payload.decode('utf-8').split("|")
    keys = ["power", "voltage", "energy", "pf", "frequency", "current"]
    pload = dict(zip(keys, values))
    print(pload)
 
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.now().replace(tzinfo=None)
    #today = today.replace(tzinfo=pytz.timezone("Europe/Kiev"))

    cursor.execute('''INSERT INTO myhome_1_electricity(param, created_date, measured_time, current, energy, voltage, frequency, pf, power) 
   VALUES (?,?,?,?,?,?,?,?,?)''', ('100', today, "",float(pload['current']),float(pload['energy']),float(pload['voltage']), float(pload['frequency']),float(pload['pf']),float(pload['power'])))
    conn.commit()
    conn.close




mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("home/poliv/water", on_message_msgs)
mqttc.message_callback_add("zigbee2mqtt/0x00124b00239e7040", on_message_bytes)
mqttc.message_callback_add("home/electro", on_message_electro)
mqttc.message_callback_add("home/electro/all", on_message_electro_all)
#mqttc.on_message = on_message
mqttc.connect("kotok.asuscomm.com", 1883, 60)
mqttc.subscribe("#", 0)

mqttc.loop_forever()
