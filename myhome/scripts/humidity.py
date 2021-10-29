import os
import time
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

try:
    f = open('/home/pi/iot/myhome/myhome/humidity.csv', 'a+')
    if os.stat('/home/pi/iot/myhome/myhome/humidity.csv').st_size == 0:
        f.write('Date,Time,Temperature,Humidity\r\n')
except:
    pass


humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if humidity is not None and temperature is not None:
    f.write('{0},{1},{2:0.1f},{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity))
    #print('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M:%S'), temperature, humidity))
else:
    print("Failed to retrieve data from humidity sensor")

