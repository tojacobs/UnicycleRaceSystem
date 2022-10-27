import enum
import time
from _thread import start_new_thread
try:
    import RPi.GPIO as GPIO  # type: ignore
    testMode = False
except ModuleNotFoundError:
    testMode = True


class Color(enum.IntEnum):
    Red = 1
    Orange = 2
    Green = 3


class TrafficLight:
    def __init__(self, GPIORed, GPIOOrange, GPIOGreen):
        self._gpio = {
            Color.Red: GPIORed,
            Color.Orange: GPIOOrange,
            Color.Green: GPIOGreen
        }
        self._colorStatus = {
            Color.Red: False,
            Color.Orange: False,
            Color.Green: False
        }
        self._blinkingActive = False
        self._threadActive = False
        self._blinkingSpeedInSec = 1
        if not testMode:
            self.setupGPIO()

    def __del__(self):
        self._blinkingActive = False
        if not testMode:
            self.cleanUpGPIO()

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        for output in self._gpio.values():
            GPIO.setup(output, GPIO.OUT)

    def cleanUpGPIO(self):
        GPIO.cleanup()

    def turnOn(self, color):
        self._colorStatus[color] = True
        self.setGPIO(color, self._colorStatus[color])

    def turnOff(self, color):
        self._colorStatus[color] = False
        self.setGPIO(color, self._colorStatus[color])

    def setBlinking(self, blinking):
        self._blinkingActive = blinking
        if blinking and not self._threadActive:
            start_new_thread(self.startBlinking, ())
            self._threadActive = True

    def setGPIO(self, color, status):
        if testMode:
            print(id(self), end=" ")
            print(color.name, end=" ")
            print("to {0}".format(status))
        else:
            GPIO.output(self._gpio[color], not (status))

    def restoreLightStatusAfterBlinking(self, tempColorStatus):
        for color in self._colorStatus:
            if (tempColorStatus[color] != self._colorStatus[color]):
                self.setGPIO(color, self._colorStatus[color])

    def startBlinking(self):
        # Create temporary statuses because we don't want to change the original statuses
        tempColorStatus = {
            Color.Red: self._colorStatus[Color.Red],
            Color.Orange: self._colorStatus[Color.Orange],
            Color.Green: self._colorStatus[Color.Green]
        }
        while self._blinkingActive:
            for color in self._colorStatus:
                if self._colorStatus[color]:
                    tempColorStatus[color] = not (tempColorStatus[color])
                    self.setGPIO(color, tempColorStatus[color])
            time.sleep(self._blinkingSpeedInSec)
        self.restoreLightStatusAfterBlinking(tempColorStatus)
        self._threadActive = False
