#!/home/pi/iot/venv/bin/python
import paho.mqtt.client as paho

def my_publish(client,userdata,result):
 
    broker="192.168.1.141"
    port=1883

    def on_publish(client,userdata,result):            
        print("data published \n")
        pass
    
    
    client1= paho.Client("control1")                            
    client1.on_publish = on_publish                          
    client1.publish("sonoff1",1) 

