import enum
import RPi.GPIO as GPIO
import time
from _thread import *


class Color(enum.IntEnum):
    Red = 0
    Orange = 1
    Green = 2

class TrafficLight:
    def __init__(self, GPIORed, GPIOOrange, GPIOGreen):
        self._gpio = [GPIORed,GPIOOrange,GPIOGreen]
        self.setupGPIO()   
        self._status = [False,False,False]
        self._blinkingActive = False
        start_new_thread(self.light_program,())

    def __del__(self):
        self.cleanUpGPIO()

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        for output in self._gpio:
            GPIO.setup(output, GPIO.OUT)

    def cleanUpGPIO(self):
        GPIO.cleanup()

    def turnOn(self, color):
        print("licht aan p" + str() + " kleur " + str(color))
        self._status[color] = True

    def turnOff(self, color):
        print("licht uit p" + str(self._gpio[0]) + " kleur " + str(color))
        self._status[color] = False;

    def setBlinking(self, blinking):
        self._blinkingActive = blinking
        if (blinking):
            print("p " + str(self._gpio[0]) +" Knipperen aan")
        else:
            print("p " + str(self._gpio[0]) +" Knipperen uit")

    def light_program(self):
        while True:
            now = int(time.time()*5)
            clock = bool(now%2)
            for color in Color:
                GPIO.output(self._gpio[color],not(self._status[color] and (not self._blinkingActive or clock)))
