from machine import Pin
from machine import Timer
from machine import RTC
import machine
import esp32
import usocket
import socket
import network
import ubinascii


#Variables
counter = 0

#Wifi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ZyXEL8B32A8', '73NHW74UKJ33X')
        while not wlan.isconnected():
            pass
    print("Oh Yes! Get connected")
    print("Connected to " + str(wlan.config("essid")))
    print("MAC Address: " + str(ubinascii.hexlify(wlan.config('mac'), ':').decode()))
    print("IP Address: " + wlan.ifconfig()[0])
    
#Connecting now to 
def getdata(counter, flag):
    if (counter < 30) & (flag == 1):
        temp = esp32.raw_temperature()
        hall = esp32.hall_sensor()
        print('Hall:'+str(hall), 'Temperature:'+str(temp))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockaddr = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
        sock.connect(sockaddr)
        sock.sendall("GET https://api.thingspeak.com/update?api_key=4XEMEDRHEKUNEHHQ&field1="+str(temp)+"&field2="+str(hall)+"HTTP/1.0\r\n\r\n")
        sock.recv(1024)
        sock.close()
    elif(counter == 30):
        flag = 0
        
def interrupthandler(counter):
    global flag
    flag = 1
    getdata(counter, flag)
#Main
#Wifi connection
connect()

#Setting up Hardware Timer - 1
tim_hardware = Timer(1)
tim_hardware.init(period = 15000, mode=Timer.PERIODIC, callback= lambda t: interrupthandler(counter))


    


