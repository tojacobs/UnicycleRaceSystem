import enum
import time
from _thread import start_new_thread
from tkinter import Tk
from tkinter import Canvas


class Color(enum.IntEnum):
    Red = 1
    Orange = 2
    Green = 3


class GraphicalTrafficLight:
    def __init__(self, name):
        self._colorStatus = {
            Color.Red: False,
            Color.Orange: False,
            Color.Green: False
        }
        self._blinkingActive = False
        self._threadActive = False
        self._blinkingSpeedInSec = 1
        self._exitThread = False
        self._queue = []
        self.createWindow()

    def __del__(self):
        self._blinkingActive = False
        self._exitThread = True

    def createWindow(self):
        self._window = Tk()
        self._window.title('Trafficlight')
        self._canvas = Canvas(self._window, width=120, height=330)
        self._red = self._canvas.create_oval(10, 10, 110, 110,fill='grey')
        self._orange = self._canvas.create_oval(10, 120, 110, 220,fill='grey')
        self._green = self._canvas.create_oval(10, 230, 110, 330,fill='grey')
        self._canvas.pack()
        print("Window created")

    def setColor(self, color, on):
        if color == Color.Red:
            if on:
                self._canvas.itemconfig(self._red, fill='Red')
            else:
                self._canvas.itemconfig(self._red, fill='Grey')
        if color == Color.Orange:
            if on:
                self._canvas.itemconfig(self._orange, fill='Orange')
            else:
                self._canvas.itemconfig(self._orange, fill='Grey')
        if color == Color.Green:
            if on:
                self._canvas.itemconfig(self._green, fill='Green')
            else:
                self._canvas.itemconfig(self._green, fill='Grey')

    def turnOn(self, color):
        self._colorStatus[color] = True
        self._queue.append([color, True])
        #self.setColor(color, True)

    def turnOff(self, color):
        self._colorStatus[color] = False
        self._queue.append([color, False])
        #self.setColor(color, False)

    def setBlinking(self, blinking):
        self._blinkingActive = blinking
        if blinking and not self._threadActive:
            start_new_thread(self.startBlinking, ())
            self._threadActive = True

    def restoreLightStatusAfterBlinking(self, tempColorStatus):
        for color in self._colorStatus:
            if (tempColorStatus[color] != self._colorStatus[color]):
                self._queue.append([color, self._colorStatus[color]])

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
                    self._queue.append([color, tempColorStatus[color]])
            time.sleep(self._blinkingSpeedInSec)
        self.restoreLightStatusAfterBlinking(tempColorStatus)
        self._threadActive = False

    def updateGUI(self):
        while len(self._queue) > 0:
            self.setColor(self._queue[0][0], self._queue[0][1])
            print("setColor {} to {}".format(self._queue[0][0], self._queue[0][1]))
            self._queue.pop()
