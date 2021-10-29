import sqlite3
from datetime import date, datetime
import paho.mqtt.client as mqtt
import time
import json
import csv

def on_message_electro_all(mosq, obj, msg):
    
    values = msg.payload.decode('utf-8').split("|")
    keys = ["power", "voltage", "energy", "pf", "frequency", "current"]
    pload = dict(zip(keys, values))
    print(pload)
 
    conn = sqlite3.connect("/home/pi/iot/myhome/db.sqlite3") 
    cursor = conn.cursor()
    today = datetime.today()
    cursor.execute('''INSERT INTO myhome_1_electricity(param, created_date, measured_time, current, energy, voltage, frequency, pf, power) 
   VALUES (?,?,?,?,?,?,?,?,?)''', ('1', today, "",float(pload['current']),float(pload['energy']),float(pload['voltage']), float(pload['frequency']),float(pload['pf']),float(pload['power'])))
   conn.commit()
   conn.close
    
    



mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("home/electro/all", on_message_electro_all)
#mqttc.on_message = on_message
mqttc.connect("kotok.asuscomm.com", 1883, 60)
mqttc.subscribe("home/electro/#", 0)

mqttc.loop_forever()
