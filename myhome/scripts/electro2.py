from socket import *      #import the socket library
from datetime import datetime
import time
import csv  
#import paho.mqtt.publish as paho


broker="192.168.1.141"
port=1883


#MY FUNCTIONS
def send(data = str):
    conn.send(data.encode())
def recieve():
    recieve.data = conn.recv(BUFSIZE) 
    recieve.data = recieve.data.decode()
    return recieve.data

##let's set up some constants
HOST = ''    #we are the host
PORT = 2000    #arbitrary port not currently in use
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 50    #reasonably sized buffer for data

serv = socket( AF_INET,SOCK_STREAM)
#serv.settimeout(None)

serv.bind((ADDR))    #the double parens are to create a tuple with one element
serv.listen(1)  #5 is the maximum number of queued connections we'll allow
serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
conn,addr = serv.accept() #accept the connection
print("Connection Established initial")
while 1:

    try:
        #send("C")
        #serv.settimeout(3)
        out = str(datetime.now())+"|"+ recieve()
        print(out)
        with open('energy.csv', 'a') as f:
            print(out, file = f)            
        #paho.single("home/electro/all",out, hostname = broker, port = port)       
        if not recieve():
            time.sleep(2)
            print("sleep")
            conn.close()
          

            
    except:
        #socket.shutdown(SHUT_RDWR)
        #conn.close()
        
        #conn,addr = serv.accept() #accept the connection
        print("reconnect")


