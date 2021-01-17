from machine import TouchPad, Pin, RTC, Timer, deepsleep
import machine
import ubinascii
import esp32
import ntptime
import network
from time import sleep

def handletouch(tim2):
    if tpin_green.read() > 500:
        green.value(0)
    else:
        green.value(1)
        
def handlesleep(tim3):
    print('I am awake, but going to deep sleep')
    red.value(0)
    green.value(0)
    # put the device to sleep for 60 seconds
    deepsleep(60000)

def printtime(datetime):
    print('Date: '+ "{:02d}".format(datetime[1])+'/'+"{:02d}".format(datetime[2])+'/'+"{:02d}".format(datetime[0]))
    print('Time: ' + "{:02d}".format(datetime[4])+':'+"{:02d}".format(datetime[5])+':'+"{:02d}".format(datetime[6])+' '+'HRS')

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

connect()

#Clock UTC time
ntptime.settime()
rtc = RTC()
year, month, day, weekday, hours, minutes, seconds, microseconds = rtc.datetime()
rtc.datetime((year, month, day, weekday, hours - 4, minutes, seconds, microseconds))
ntptime.host = "pool.ntp.org"

#Hardware timer - 1
tim1 = Timer(1)
tim1.init(period=15000, mode=Timer.PERIODIC, callback=lambda t:printtime(rtc.datetime()))

#Variables
#LEDs
green = Pin(21, Pin.OUT)
red = Pin(32, Pin.OUT)

#Buttons
button_red = Pin(25, Pin.IN, Pin.PULL_DOWN)
button_green = Pin(26, Pin.IN, Pin.PULL_DOWN)

#Touchpad
tpin = TouchPad(Pin(27))
tpin_green = TouchPad(Pin(33))

# configure the threshold at which the pin is considered touched
tpin.config(500)
esp32.wake_on_touch(True)

#External button wake-up
esp32.wake_on_ext1(pins = (button_red, button_green), level = esp32.WAKEUP_ANY_HIGH)

#Red led turns on
red.value(1)

#Hardware timer - 2
tim2 = Timer(2)
tim2.init(period=10, mode=Timer.PERIODIC, callback=handletouch)

# #Hardware timer - 3
tim3 = Timer(3)
tim3.init(period=30000, mode=Timer.PERIODIC, callback=handlesleep)

# check if the device woke from a deep sleep
if machine.wake_reason() == 5:
    print('Touchpad Wake-up') 
elif machine.wake_reason() == 3:
    print('EXT1 Wake-up')
elif machine.wake_reason() == 4:
    print('Timer Wake-up')

    
