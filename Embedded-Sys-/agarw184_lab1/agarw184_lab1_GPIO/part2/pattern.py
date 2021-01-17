from machine import Pin
from time import sleep

#Pins for buttons 
button1 = Pin(14, Pin.IN)         #Red
button2 = Pin(32,Pin.IN)          #Green

#Output pins for red and green led respectively.
red = Pin(15,Pin.OUT)
green = Pin(21,Pin.OUT)

#Setting the LEDs 
red.value(0)
green.value(0)

#Counter variables
cnt1 = 0            #Red 
cnt2 = 0            #Green

#Loop to facilitate push button blinking
while(True):
    sleep(0.2)
    if button1.value() == 0 and button2.value() == 0:
        #1st case
        red.value(0)
        green.value(0)
        
    elif button1.value() == 0 and button2.value() == 1:
        #2nd case"
        cnt2 = cnt2 + 1
        red.value(0)
        green.value(1)
    elif button1.value() == 1 and button2.value() == 0:
        #3rd case
        cnt1 = cnt1 + 1
        red.value(1)
        green.value(0)
    elif button1.value() == 1 and button2.value() == 1:
        #4th case
        cnt1 = cnt1 + 1
        cnt2 = cnt2 + 1
        red.value(0)
        green.value(0)

#Loops to facilitate alternative blinking
    if cnt1 >= 10 or cnt2 >= 10:
        if (cnt1 >= 10):
            while(True):
                red.value(1)
                green.value(0)
                sleep(0.5)
                red.value(0)
                green.value(1)
                sleep(0.5)
                #When the other button is pressed 
                if button2.value():
                    red.value(0)
                    green.value(0)
                    print('You have successfully implemented LAB1 DEMO!!!')
                    break
            break
                    
        if (cnt2 >= 10):
            while(True):
                red.value(1)
                green.value(0)
                sleep(0.5)
                red.value(0)
                green.value(1)
                sleep(0.5)
                if button1.value():
                    red.value(0)
                    green.value(0)
                    print('You have successfully implemented LAB1 DEMO!!!')
                    break
            break
        
#End of Code       
        