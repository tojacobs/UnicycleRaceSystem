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
        self._colorStatus =	{
            Color.Red : False,
            Color.Orange: False,
            Color.Green: False
        }
        self._blinkingActive = False

    def __del__(self):
        self.cleanUpGPIO()

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        for output in self._gpio:
            GPIO.setup(output, GPIO.OUT)

    def cleanUpGPIO(self):
        GPIO.cleanup()

    def turnOn(self, color):
        self._colorStatus[color] = True
        GPIO.output(self._gpio[color], not(self._colorStatus[color]))

    def turnOff(self, color):
        self._colorStatus[color] = False;
        GPIO.output(self._gpio[color], not(self._colorStatus[color]))

    def setBlinking(self, blinking):
        self._blinkingActive = blinking
        if blinking:
            start_new_thread(self.startBlinking,())

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
            time.sleep(1)
        # Restore original status after blinking is turned off
        for color in self._colorStatus:
            if (tempColorStatus[color] != self._colorStatus[color]):
                GPIO.output(self._gpio[color], not(self._colorStatus[color]))
