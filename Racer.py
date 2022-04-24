from trafficLight import *

class Racer:
    def __init__(self, Name, GPIORed, GPIOOrange, GPIOGreen):
        self._name = Name
        self._startTimeInMs = None
        self._finishTimeInMs = None
        self._falseStart = False
        self._finished = False
        self._light = TrafficLight(GPIORed, GPIOOrange, GPIOGreen)

    def reset(self):
        self._startTimeInMs = None
        self._finishTimeInMs = None
        self._falseStart = False
        self._finished = False
        self._light.turnOff(Color.Orange)
        self._light.turnOff(Color.Green)
        self._light.turnOn(Color.Red)
        self._light.setBlinking(False)

    def setName(self, Name):
        self._name = Name

    def getName(self):
        return self._name

    def setStartTime(self, startTime):
        self._startTimeInMs = startTime

    def setFinishTime(self, finishTime):
        self._finishTimeInMs = finishTime
        self._finished = True

    def setFalseStart(self, falseStart):
        self._falseStart = falseStart
        self._finished = True
        self._light.setBlinking(True)

    def getFalseStart(self):
        return self._falseStart

    def getFinished(self):
        return self._finished

    def startRace(self):
        if (not self._falseStart):
            self._light.turnOn(Color.Green)
            self._light.turnOff(Color.Red)
            self._light.turnOff(Color.Orange)

    def getRaceTime(self):
        if (self._finished and not self._falseStart):
            timeMs = self._finishTimeInMs*1000 - self._startTimeInMs*1000
            seconds=(timeMs/1000)%60
            minutes=(timeMs/(1000*60))%60
            return minutes, seconds

    def printResult(self):
        if (self._finished and not self._falseStart):
            minutes, seconds = self.getRaceTime()
            return "Tijd %s: %d:%.3f" % (self._name, int(minutes), seconds)
        elif (self._falseStart):
            return "Valse start %s" % (self._name)
