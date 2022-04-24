import enum

class Color(enum.Enum):
    Red = 1
    Orange = 2 
    Green = 3

class TrafficLight:
    def __init__(self, GPIORed, GPIOOrange, GPIOGreen):
        self._gpioRed = GPIORed
        self._gpioOrange = GPIOOrange
        self._gpioGreen = GPIOGreen
        self.turnOff(Color.Red)
        self.turnOff(Color.Orange)
        self.turnOff(Color.Green)
        self.setBlinking(False)

    def turnOn(self, color):
        print("licht aan p" + str(self._gpioRed) + " kleur " + str(color))

    def turnOff(self, color):
        print("licht uit p" + str(self._gpioRed) + " kleur " + str(color))

    def setBlinking(self, blinking):
        if (blinking):
            print("p " + str(self._gpioRed) +" Knipperen aan")
        else:
            print("p " + str(self._gpioRed) +" Knipperen uit")
