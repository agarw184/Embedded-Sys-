import machine
from machine import RTC, Pin, PWM, Timer, ADC
from time import sleep

#Real-Time Clock
rtc = RTC()

#Questions
#Prior starting the main program
year = int(input("Year?"))
month = int(input("Month?"))
day = int(input("Day?"))
weekday = int(input("Weekday?"))
hour = int(input("Hour?"))
minute = int(input("Minute?"))
sec = int(input("Second?"))
microsec = int(input("Microsecond?"))
rtc.datetime((year, month, day, weekday, hour, minute, sec, microsec))

#Setting up PWM
red_pwm = PWM(Pin(32), freq=10, duty=256)
green_pwm = PWM(Pin(21), freq=10, duty=256)

#Variables
button_press = 0
flag = True

#Introduces delay for debounce
def delay(tim_button):
    global flag
    flag = True

#Button interrupt handler 
def handle_interrupt(pin):
    global flag
    global button_press
    if flag == True:
        flag = False
        button_press = button_press + 1
     #   print("Button Pressed", button_press)

#Setting  up ADC
adc = ADC(Pin(33))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

#Detect switch press using IRQ
#Keeps track of which press it is
button1 = Pin(14, Pin.IN, Pin.PULL_UP)
button1.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

#Setting up Hardware Timer - 1
tim_hardware = Timer(1)
tim_hardware.init(period = 30000, mode=Timer.PERIODIC, callback=lambda t:(print(rtc.datetime())))

#Setting up Software Timer/ Hardware Timer - 1
tim_software = Timer(2)
tim_software.init(period = 100, mode=Timer.PERIODIC, callback=lambda t:(print(adc.read())))

#Timer for button
tim_button = Timer(3)
tim_button.init(period = 300, mode=Timer.PERIODIC, callback=delay)

while True:

    if(flag):
        if((button_press % 2) != 0):
            pot_value = adc.read()
            red_pwm.freq(pot_value)
            sleep(0.5)
        elif((button_press % 2) == 0):
            pot_value = adc.read()
            green_pwm.duty(pot_value)
            sleep(0.5)
    else:
        flag = False