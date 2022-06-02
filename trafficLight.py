import enum
import RPi.GPIO as GPIO
import time
from _thread import *

class Color(enum.IntEnum):
    Red = 1
    Orange = 2
    Green = 3

class TrafficLight:
    def __init__(self, GPIORed, GPIOOrange, GPIOGreen):
        self._gpio = {
            Color.Red : GPIORed,
            Color.Orange: GPIOOrange,
            Color.Green: GPIOGreen
        }
        self._colorStatus =	{
            Color.Red : False,
            Color.Orange: False,
            Color.Green: False
        }
        self._blinkingActive = False
        self._threadActive = False
        self.setupGPIO()

    def __del__(self):
        self.cleanUpGPIO()
        self._blinkingActive = False

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        for output in self._gpio.values():
            GPIO.setup(output, GPIO.OUT)

    def cleanUpGPIO(self):
        GPIO.cleanup()

    def turnOn(self, color):
        self._colorStatus[color] = True
        GPIO.output(self._gpio[color], not(self._colorStatus[color]))
        #print("Set {0} to {1}".format(self._gpio[color], self._colorStatus[color]))

    def turnOff(self, color):
        self._colorStatus[color] = False
        GPIO.output(self._gpio[color], not(self._colorStatus[color]))
        #print("Set {0} to {1}".format(self._gpio[color], self._colorStatus[color]))

    def setBlinking(self, blinking):
        self._blinkingActive = blinking
        if blinking and not self._threadActive:
            start_new_thread(self.startBlinking,())
            self._threadActive = True

    def startBlinking(self):
        # Create temporary statuses because we don't want to change the original statuses
        tempColorStatus =	{
            Color.Red : self._colorStatus[Color.Red],
            Color.Orange: self._colorStatus[Color.Orange],
            Color.Green: self._colorStatus[Color.Green]
        }
        while self._blinkingActive:
            for color in self._colorStatus:
                if self._colorStatus[color]:
                    tempColorStatus[color] = not(tempColorStatus[color])
                    GPIO.output(self._gpio[color], not(tempColorStatus[color]))
                    #print("Set {0} to {1}".format(self._gpio[color], tempColorStatus[color]))
            time.sleep(1)
        # Restore original status after blinking is turned off
        for color in self._colorStatus:
            if (tempColorStatus[color] != self._colorStatus[color]):
                GPIO.output(self._gpio[color], not(self._colorStatus[color]))
                #print("Reseting {0} to {1}".format(self._gpio[color], self._colorStatus[color]))
        self._threadActive = False
