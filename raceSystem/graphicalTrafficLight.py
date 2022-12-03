import time
from _thread import start_new_thread
from raceSystem.RPiTrafficLight import testMode
from raceSystem.iTrafficLight import iTrafficLight
from raceSystem.iTrafficLight import Color

# Check for testMode in order to not have to install pysimplegui on the RPi's
if testMode:
    import PySimpleGUI as sg


class GraphicalTrafficLight(iTrafficLight):
    def __init__(self, name):
        self._colorStatus = {
            Color.Red: False,
            Color.Orange: False,
            Color.Green: False
        }
        self._blinkingActive = False
        self._threadActive = False
        self._blinkingSpeedInSec = 1
        self._queue = []
        self._name = name
        self.createWindow()

    def __del__(self):
        self._blinkingActive = False

    def createWindow(self):
        layout = [[sg.Canvas(size=(120, 340), key='canvas')]]
        self._window = sg.Window(self._name, layout, finalize=True)
        self._canvas = self._window['canvas']
        self._canvas.TKCanvas.create_text(60, 10, text=self._name)
        self._red = self._canvas.TKCanvas.create_oval(10, 20, 110, 110, fill='grey')
        self._orange = self._canvas.TKCanvas.create_oval(10, 130, 110, 220, fill='grey')
        self._green = self._canvas.TKCanvas.create_oval(10, 240, 110, 330, fill='grey')
        self._window.refresh()

    def setColor(self, color, on):
        if color == Color.Red:
            if on:
                self._canvas.TKCanvas.itemconfig(self._red, fill='Red')
            else:
                self._canvas.TKCanvas.itemconfig(self._red, fill='Grey')
        if color == Color.Orange:
            if on:
                self._canvas.TKCanvas.itemconfig(self._orange, fill='Orange')
            else:
                self._canvas.TKCanvas.itemconfig(self._orange, fill='Grey')
        if color == Color.Green:
            if on:
                self._canvas.TKCanvas.itemconfig(self._green, fill='Green')
            else:
                self._canvas.TKCanvas.itemconfig(self._green, fill='Grey')
        self._window.refresh()

    def turnOn(self, color):
        self._colorStatus[color] = True
        self._queue.append([color, True])

    def turnOff(self, color):
        self._colorStatus[color] = False
        self._queue.append([color, False])

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
            self._queue.pop(0)
