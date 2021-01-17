import machine
from machine import Pin
from machine import I2C
from machine import Timer
from machine import PWM
from math import atan
from math import degrees
from math import pow
from math import sqrt
import esp32
import usocket
import socket
import network
import ubinascii
import urequests

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Delhi Belly', 'apgdgr88')
        while not wlan.isconnected():
            pass
    print("Oh Yes! Get connected")
    print("Connected to " + str(wlan.config("essid")))
    print("MAC Address: " + str(ubinascii.hexlify(wlan.config('mac'), ':').decode()))
    print("IP Address: " + wlan.ifconfig()[0])
    

class MPU:
    # Static MPU memory addresses
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        # Accelerometer by default is set to 2g sensitivity setting
        # 1g = 9.81 m/s^2 = 16384 according to mpu datasheet
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81

        return acc_x, acc_y, acc_z

    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()

        temp = self.__bytes_to_int(temp)
        return self.__celsius_to_fahrenheit(temp / 340 + 36.53)

    def gyro(self):
        return self.pitch, self.roll, self.theta

    def __init_gyro(self):
        # MPU must be stationary
        gyro_offsets = self.__read_gyro()
        self.pitch_offset = gyro_offsets[1]
        self.roll_offset = gyro_offsets[0]
        self.theta_offset = gyro_offsets[2]

    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()

        # Gyro by default is set to 250 deg/sec sensitivity
        # Gyro register values return angular velocity
        # We must first scale and integrate these angular velocities over time before updating current pitch/roll/yaw
        # This method will be called every 100ms...
        gyro_x = self.__bytes_to_int(gyro_x) / 250 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 250 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 250 * 0.1

        return [gyro_x, gyro_y, gyro_z]

    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.pitch += gyro_val[1] - self.pitch_offset
        self.roll += gyro_val[0] - self.roll_offset
        self.theta += gyro_val[2] - self.theta_offset

    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp * 9 / 5 + 32

    @staticmethod
    def __bytes_to_int(data):
        # Int range of any register: [-32768, +32767]
        # Must determine signing of int
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def __init__(self, i2c):
        # Init MPU
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        print('Initialized MPU6050.')

# Gyro values will be updated every 100ms after creation of MPU object
        self.pitch = 0
        self.roll = 0
        self.theta = 0
	self.pitch_offset = 0
        self.roll_offset = 0
        self.theta_offset = 0
        self.__init_gyro()
        gyro_timer = Timer(3)
        gyro_timer.init(mode=Timer.PERIODIC, callback=self.__update_gyro, period=100)

#Main
#LED defs 
LED = Pin(13, Pin.OUT)
redLED = Pin(14, Pin.OUT)
yellowLED = Pin(15, Pin.OUT)
greenLED = Pin(12, Pin.OUT)

#Button defs 
button1 = Pin(4, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(21, Pin.IN, Pin.PULL_DOWN)

#SessionID definition
SessionID = 123456

#url
url = 'https://maker.ifttt.com/trigger/spinner_lab6/with/key/ni_SXPLrouMl20ctxsuGGvP3uxJ6vcjGgNJrSI65maS'

#I2c and mpu class usage
i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)
mpu = MPU(i2c)

#Timer defs
tim1 = Timer(1)
tim2 = Timer(2)



#Button functions 
def button_1():
    print("Button-1 Pressed")
    LED.value(1)
    greenLED.value(0)
    redLED.value(0)
    yellowLED.value(0)

    print('Acceleration along X, Y and Z axis respectively is : ', mpu.acceleration())
    print('Temperature in (F) is: ',mpu.temperature())
    print('Gyroscope values along X, Y and Z axis respectively is: ',mpu.gyro())
    
    
def button1_interrupt(button1):
    tim1.init(mode=Timer.ONE_SHOT, period = 200, callback=lambda t:button_1())
    
    
def button_2():
    global flag
    print("Button-2 pressed")
    LED.value(0)
    #PWM setup
    pwm = PWM(Pin(13), freq=10, duty=512)
    initialtemp = mpu.temperature()
    
    while True and button1.value() == 0:
        flag = 1
        #Acceleration conversion to velocity
        acceleration = mpu.acceleration()
        Ax = acceleration[0]
        Ay = acceleration[1]
        Az = acceleration[2]
        
        #v = u + a*t, here u = 0, a = A corresponding to the axis and t = 1 sec. 
        Vx = Ax * 1
        Vy = Ay * 1
        Vz = (Az - 9.81) * 1
        
        print("velocity in X axis is (per sec)" + str(Vx))
        print("velocity in Y axis is (per sec)" + str(Vy))
        print("velocity in Z axis is (per sec)" + str(Vz))
        
        if(abs(Vx) > 3 or abs(Vy) > 3 or abs(Vz) > 3):
            redLED.value(1)
        else:
            redLED.value(0)
            
        #Pitch, Roll and Theta
        gyro_mpu = mpu.__read_gyro()
        Pitch = gyro_mpu[0]
        Roll = gyro_mpu[1]
        Theta = gyro_mpu[2]
        
        #Essnetial conversion required
        Pitch = degrees(atan(Ax/sqrt(pow(Ay, 2) + pow(Az, 2)))) 
        Roll = degrees(atan(Ay/sqrt(pow(Ax, 2) + pow(Az, 2))))
        Theta = degrees(atan(sqrt(pow(Ax, 2) + pow(Ay, 2)) / Az))
        
        print("Pitch is " + str(Pitch))
        print("Roll is " + str(Roll))
        print("Theta is " + str(Theta))
        
        ret = (abs(Pitch) > 30 or abs(Roll) > 30 or abs(Theta) > 30) #Better way of expressing return values 
        if ret:
            yellowLED.value(1)
        else:
            yellowLED.value(0)
        
        #Temperature stuff
        temp = mpu.temperature()
        print("Current Temperature is " + str(temp) + " degree F")
        if ((temp - initialtemp)) >= 1:
            pwm.freq(pwm.freq() + int(temp - initialtemp)*5)
        elif ((temp - initialtemp)) <= -1:
            pwm.freq(pwm.freq() - int(temp - initialtemp)*5)
        initialtemp = temp
        
        #GreenLED stuff
        greenret = (Vx == 0.0 and Vy == 0.0 and Vz == 0.0 and Pitch == 0.0 and Roll == 0.0 and Theta == 0.0)
        if greenret:
            
            greenLED.value(1)
        else:
            greenLED.value(0)
        
    if button1.value() == 1:
        pwm.deinit()
        button1_interrupt(button1)    
    
def fttt(tim3):   
    #Remember we are assuming u = 0, t = 1. Therefore my velocities would be equal to acceleration.
    #Therefore, instead of creating the vector I used my function and math here.
    global SessionID
    ifttt_data_send = {'value1': str(SessionID),'value2': str(mpu.acceleration()) + "|||" + str(mpu.__read_gyro()), 'value3': str(mpu.temperature())}
    object_headers = {'Content-Type': 'application/json'}
    request = urequests.post(url, json=ifttt_data_send, headers=object_headers)
    if request is not None and request.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
    SessionID = SessionID + 1
    request.close()
def button2_interrupt(button2):

    tim2.init(mode=Timer.ONE_SHOT, period = 200, callback= lambda t:button_2())
    tim3.init(mode=Timer.PERIODIC, period = 60000, callback = fttt(tim3))
    

#Main function
#Connect to Wifi
connect()
#Button interrupts
button1.irq(trigger=Pin.IRQ_RISING, handler = button1_interrupt)
button2.irq(trigger=Pin.IRQ_RISING, handler = button2_interrupt)
tim3 = Timer(-1)







    






