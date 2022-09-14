import time
import datetime
from state import State
from trafficLight import *
from Racer import Racer
  
class RaceSequence:
    def __init__(self):
        self._status = State.WaitingForCountDown
        self._countdown = 4
        self._orangeLightAt = 2
        self._racers = [Racer("P1", 17, 27, 22), Racer("P2", 23, 24, 25)]
        self._exit = False
        self._stop = False

    def setCallbackFunctions(self, countDownStartedCallback, countdownEndedCallback, raceEndedCallback, sendResultCallback):
        """setCallbackFunctions sets the callback functions that are being used by raceSequence"""
        self.countDownStartedCallback = countDownStartedCallback
        self.countdownEndedCallback   = countdownEndedCallback
        self.raceEndedCallback        = raceEndedCallback
        self.sendResultCallback       = sendResultCallback

    def exit(self):
        """exit is a callback function that will be called from UnicycleRaceSystem"""
        self._exit = True

    def setName(self, index, name):
        """setName is a callback function that will be called from UnicycleRaceSystem"""
        self._racers[index].setName(name)

    def getName(self, index):
        """getName is a callback function that will be called from UnicycleRaceSystem"""
        return self._racers[index].getName()

    def setCountdown(self, seconds):
        """setCountdown is a callback function that will be called from UnicycleRaceSystem"""
        self._countdown = seconds

    def getCountdown(self):
        """getCountdown is a callback function that will be called from UnicycleRaceSystem"""
        return self._countdown

    def setOrangeLightAt(self, seconds):
        """setOrangeLightAt is a callback function that will be called from UnicycleRaceSystem"""
        self._orangeLightAt = seconds

    def getOrangeLightAt(self):
        """getOrangeLightAt is a callback function that will be called from UnicycleRaceSystem"""
        return self._orangeLightAt

    def stopRace(self):
        """stopRace is a callback function that will be called from UnicycleRaceSystem"""
        self._stop = True

    def processEndTime(self, data, racer, index):
        if not (racer.getFalseStart() or racer.getFinished() or racer.getDNF()):
            data = data.split(':')[1]
            racer.setFinishTime(float(data)/1000)
            self.sendResultCallback(index, racer.getFinished(), racer.getFalseStart(), racer.getDNF(), racer.getRaceTime())
        self.endRaceIfNeeded()

    def endRaceIfNeeded(self):
        endRace = []
        for racer in self._racers:
            if (racer.getFinished() or racer.getFalseStart() or racer.getDNF()):
                endRace.append(True)
            else:
                endRace.append(False)
        if all(endRace):
            self._status = State.RaceFinished

    def processFalseStart(self, data, racer, index):
        racer.setFalseStart(True)
        self.sendResultCallback(index, racer.getFinished(), racer.getFalseStart(), racer.getDNF(), racer.getRaceTime())
        self.endRaceIfNeeded()

    def processReceivedData(self, data):
        """processReceivedData is a callback function that will be called from UnicycleRaceSystem"""
        if self._status == State.CountingDown:
            if (data.startswith("p1StartClient")):
                self.processFalseStart(data, self._racers[0], 0)
            elif (data.startswith("p2StartClient")):
                self.processFalseStart(data, self._racers[1], 1)
        elif self._status == State.RaceStarted:
            if (data.startswith("p1FinishClient")):
                self.processEndTime(data, self._racers[0], 0)
            elif (data.startswith("p2FinishClient")):
                self.processEndTime(data, self._racers[1], 1)

    def startCountdown(self, t):
        while t:
            time.sleep(1)
            t -= 1
            if (t == self._orangeLightAt):
                for racer in self._racers:
                    if not (racer.getFalseStart()):
                        racer._light.turnOn(Color.Orange)
                        racer._light.turnOff(Color.Red)

    def registerDNFs(self):
        self._stop = False
        for tuple in enumerate(self._racers):
            index, racer = tuple
            if not (racer.getFinished() or racer.getFalseStart() or racer.getDNF()):
                racer.setDNF()
            if racer.getDNF():
                self.sendResultCallback(index, racer.getFinished(), racer.getFalseStart(), racer.getDNF(), racer.getRaceTime())
        self.endRaceIfNeeded()

    def startRace(self):
        """startRace is a callback function that will be called from UnicycleRaceSystem"""
        self._status = State.WaitingForCountDown
        for racer in self._racers:
            racer.reset()
        self.countDownStartedCallback()
        self._status = State.CountingDown
        self.startCountdown(self._countdown)
        if (not self._status == State.RaceFinished):
            self._status = State.RaceStarted
            startTime = time.time()
            self.countdownEndedCallback()
            for racer in self._racers:
                racer.startRace()
                racer.setStartTime(startTime)

        while (not self._status == State.RaceFinished) and (not self._exit) and (not self._stop):   
            time.sleep(1)
        if self._stop:
            self.registerDNFs()
        self.raceEndedCallback()
