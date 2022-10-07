import enum

class Color(enum.IntEnum):
    Red = 1
    Orange = 2
    Green = 3

class TrafficLightMock:
    def __init__(self):
        self.resetForNextTest()

    def resetForNextTest(self):
        self._colorStatus =	{
            Color.Red : False,
            Color.Orange: False,
            Color.Green: False
        }
        self._blinkingActive = False
        self._threadActive = False

    def turnOn(self, color):
        self._colorStatus[color] = True
        print("TurnOn called for Color %s" % color.name)

    def turnOff(self, color):
        self._colorStatus[color] = False
        print("TurnOff called for Color %s" % color.name)

    def setBlinking(self, blinking):
        self._blinkingActive = blinking
        print("setBlinking called with parameter %s" % str(blinking))
