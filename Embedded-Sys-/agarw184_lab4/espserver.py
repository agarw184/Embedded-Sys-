# # Global variables
# TEMP  # measure temperature sensor data
# HALL  # measure hall sensor data
# RED_LED_STATE # string, check state of red led, ON or OFF
# GREEN_LED_STATE # string, check state of red led, ON or OFF

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
green = Pin(21, Pin.OUT)
red = Pin(32, Pin.OUT)

#Bonus Switch
button_red = Pin(25, Pin.IN, Pin.PULL_DOWN)
button_green = Pin(26, Pin.IN, Pin.PULL_DOWN)

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    TEMP, HALL, RED_LED_STATE, GREEN_LED_STAT
    """
    temp = (esp32.raw_temperature())
    hall = (esp32.hall_sensor())

    #For RED
    if red.value() == 0:
        RED_LED_STATE = "OFF"
    else:
        RED_LED_STATE = "ON"
        
    #For GREEN
    if green.value() == 0:
        GREEN_LED_STATE = "OFF"
    else:
        GREEN_LED_STATE = "ON"
    
    red_led_state = RED_LED_STATE
    green_led_state = GREEN_LED_STATE
    
        #Red switch
    if (button_red.value() == 1):
        switch_red_state = 'ON'
    else:
        switch_red_state = 'OFF'
    
    #Green switch
    if (button_green.value() == 1):
        switch_green_state = 'ON'
    else:
        switch_green_state = 'OFF'
    
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    <p>
    Red Switch Current State: <strong>""" + switch_red_state + """</strong>
    </p>
    <p>
    Green Switch Current State: <strong>""" + switch_green_state + """</strong>
    </p>
    </body>
    </html>"""
    return html_webpage

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
        
#Variables
#LEDs
connect()
temp = str(esp32.raw_temperature())
hall = str(esp32.hall_sensor())

#Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 80))
sock.listen(5)

while True:
    cl, addr = sock.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    
    #LED stuff
    red_led_on = request.find('/?red_led=on')
    red_led_off = request.find('/?red_led=off')
    green_led_on = request.find('/?green_led=on')
    green_led_off = request.find('/?green_led=off')

    if red_led_on == 6:
        print('RED LED ON')
        red.value(1)
        RED_LED_STATE = "ON"
        
    if red_led_off == 6:
        print('RED LED OFF')
        red.value(0)
        RED_LED_STATE = "OFF"
      
    if green_led_on == 6:
        print('GREEN LED ON')
        green.value(1)
        GREEN_LED_STATE = "ON"
        
    if green_led_off == 6:
        print('GREEN LED OFF')
        green.value(0)
        GREEN_LED_STATE = "OFF"
    
    #Reading values
    response = web_page()
    
    cl.send('HTTP/1.1 200 OK\n')
    cl.send('Content-Type: text/html\n')
    cl.send('Connection: close\n\n')
    cl.sendall(response)
    cl.close()
        
    


