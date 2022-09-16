from trafficLight import *

class Racer:
    def __init__(self, Name, GPIORed, GPIOOrange, GPIOGreen):
        self._name = Name
        self._startTimeInMs = None
        self._finishTimeInMs = None
        self._falseStart = False
        self._finished = False
        self._DNF = False
        self._startLineTimeInMs = None
        self._light = TrafficLight(GPIORed, GPIOOrange, GPIOGreen)

    def reset(self):
        self._startTimeInMs = None
        self._finishTimeInMs = None
        self._falseStart = False
        self._finished = False
        self._light.turnOff(Color.Orange)
        self._light.turnOff(Color.Green)
        self._light.turnOff(Color.Red)
        self._light.setBlinking(False)
        self._DNF = False
        self._startLineTimeInMs = None

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

    def getFalseStart(self):
        return self._falseStart

    def getFinished(self):
        return self._finished

    def getDNF(self):
        return self._DNF

    def setDNF(self):
        self._DNF = True

    def setReactionTime(self, reactionTime):
        self._startLineTimeInMs = reactionTime

    def getReactionTimeInMS(self):
        if self._startLineTimeInMs != None:
            timeMs = self._startLineTimeInMs*1000 - self._startTimeInMs*1000
            return int(timeMs)
        else:
            return None

    def countDownStarted(self):
        self._light.turnOn(Color.Red)

    def swithToOrange(self):
        if (not self._falseStart):
            self._light.turnOn(Color.Orange)
            self._light.turnOff(Color.Red)

    def startRace(self):
        if (not self._falseStart):
            self._light.turnOn(Color.Green)
            self._light.turnOff(Color.Red)
            self._light.turnOff(Color.Orange)
        else:
            self._light.setBlinking(True)

    def getRaceTime(self):
        if (not self._DNF):
            timeMs = self._finishTimeInMs*1000 - self._startTimeInMs*1000
            seconds=(timeMs/1000)%60
            minutes=(timeMs/(1000*60))%60
            return minutes, seconds
        else:
            return 0, 0
