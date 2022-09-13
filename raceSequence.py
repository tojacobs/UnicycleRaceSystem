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

    def exit(self):
        self._exit = True

    def setCallbackFunctions(self, displayCallback):
        self.display = displayCallback

    def processEndTime(self, data, racer):
        if not (racer.getFalseStart() or racer.getFinished()):
            data = data.split(':')[1]
            racer.setFinishTime(float(data)/1000)
            self.display(racer.printResult())
        self.endRaceIfNeeded()

    def endRaceIfNeeded(self):
        endRace = []
        for racer in self._racers:
            if (racer.getFinished() or racer.getFalseStart()):
                endRace.append(True)
            else:
                endRace.append(False)
        if all(endRace):
            self._status = State.RaceFinished

    def processFalseStart(self, data, racer):
        racer.setFalseStart(True)
        self.display(racer.printResult())
        self.endRaceIfNeeded()

    def processReceivedData(self, data):
        if self._status == State.CountingDown:
            if (data.startswith("p1StartClient")):
                self.processFalseStart(data, self._racers[0])
            elif (data.startswith("p2StartClient")):
                self.processFalseStart(data, self._racers[1])
        elif self._status == State.RaceStarted:
            if (data.startswith("p1FinishClient")):
                self.processEndTime(data, self._racers[0])
            elif (data.startswith("p2FinishClient")):
                self.processEndTime(data, self._racers[1])

    def startCountdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.display(timer, end="\r")
            time.sleep(1)
            t -= 1
            if (t == self._orangeLightAt):
                for racer in self._racers:
                    if not (racer.getFalseStart()):
                        racer._light.turnOn(Color.Orange)
                        racer._light.turnOff(Color.Red)

    def startRace(self):
        self._status = State.WaitingForCountDown
        #self.waitForClients()
        for racer in self._racers:
            racer.reset()
        self.display("\nNieuwe race gestart! Countdown is begonnen!")
        self._status = State.CountingDown
        self.startCountdown(self._countdown)
        if (not self._status == State.RaceFinished):
            self._status = State.RaceStarted
            startTime = time.time()
            self.display('GO!  ')
            for racer in self._racers:
                racer.startRace()
                racer.setStartTime(startTime)
            self.display("Starttijd: " + datetime.datetime.fromtimestamp(time.time()).ctime())

        while (not self._status == State.RaceFinished) and (not self._exit):    
            time.sleep(1)
        self.display("Race gefinished, type een commando...")
