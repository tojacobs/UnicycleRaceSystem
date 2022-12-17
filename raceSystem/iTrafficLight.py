import abc
import enum


class Color(enum.IntEnum):
    Red = 1
    Orange = 2
    Green = 3


class iTrafficLight(abc.ABC):
    @abc.abstractmethod
    def __del__(self):
        """destructor methon must set blinking to false."""
        pass

    @abc.abstractmethod
    def turnOn(self, color):
        """The light for the given color will be turned on."""
        pass

    @abc.abstractmethod
    def turnOff(self, color):
        """The light for the given color will be turned off."""
        pass

    @abc.abstractmethod
    def setBlinking(self, blinking):
        """Turn blinking on or off for the colors that are currently on.
        Colors that are turned on while blinking is active will also start blinking."""
        pass
