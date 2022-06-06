
class Racer:
    def __init__(self, Name):
        self._name = Name
        self._startTimeInMs = None
        self._startLineTimeInMs = None
        self._finishTimeInMs = None

    def reset(self):
        self._startTimeInMs = None
        self._startLineTimeInMs = None
        self._finishTimeInMs = None

    def setName(self, Name):
        self._name = Name

    def getName(self):
        return self._name

    def setStartTime(self, startTime):
        self._startTimeInMs = startTime

    def setStartLineTime(self, startTime):
            self._startLineTimeInMs = startTime

    def setFinishTime(self, finishTime):
            self._finishTimeInMs = finishTime

    def getFalseStart(self):
        if (self._startTimeInMs != None and self._startLineTimeInMs != None):
            return self._startTimeInMs > self._startLineTimeInMs
        else:
            return False

    def getFinished(self):
        return self._finishTimeInMs != None

    def RaceIsStarted(self):
        return self._startTimeInMs != None

    def RaceIsOver(self):
        return self.getFinished() or self.getFalseStart()

    def getRaceTime(self):
        if (self.getFinished and not self.getFalseStart):
            timeMs = self._finishTimeInMs*1000 - self._startTimeInMs*1000
            seconds=(timeMs/1000)%60
            minutes=(timeMs/(1000*60))%60
            return minutes, seconds
