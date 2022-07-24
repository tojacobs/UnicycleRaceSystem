import time
import datetime
from state import State
from trafficLight import *
from Racer import Racer
  
class RaceSequence:
    def __init__(self):
        self.status = State.WaitingForCountDown
        self.countdown = 3
        self.orangeLightAt = 1
        self.racers = [Racer("P1", 17, 27, 22), Racer("P2", 23, 24, 25)]
        self.exit = False

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
        for racer in self.racers:
            if (racer.getFinished() or racer.getFalseStart()):
                endRace.append(True)
            else:
                endRace.append(False)
        if all(endRace):
            self.status = State.RaceFinished

    def processFalseStart(self, data, racer):
        racer.setFalseStart(True)
        self.display(racer.printResult())
        self.endRaceIfNeeded()

    def processReceivedData(self, data):
        if self.status == State.CountingDown:
            if (data.startswith("p1StartClient")):
                self.processFalseStart(data, self.racers[0])
            elif (data.startswith("p2StartClient")):
                self.processFalseStart(data, self.racers[1])
        elif self.status == State.RaceStarted:
            if (data.startswith("p1FinishClient")):
                self.processEndTime(data, self.racers[0])
            elif (data.startswith("p2FinishClient")):
                self.processEndTime(data, self.racers[1])

    def startCountdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.display(timer, end="\r")
            time.sleep(1)
            t -= 1
            if (t == self.orangeLightAt):
                for racer in self.racers:
                    if not (racer.getFalseStart()):
                        racer._light.turnOn(Color.Orange)
                        racer._light.turnOff(Color.Red)

    def startRace(self):
        self.status = State.WaitingForCountDown
        #self.waitForClients()
        for racer in self.racers:
            racer.reset()
        self.display("\nNieuwe race gestart! Countdown is begonnen!")
        self.status = State.CountingDown
        self.startCountdown(self.countdown)
        if (not self.status == State.RaceFinished):
            self.status = State.RaceStarted
            startTime = time.time()
            self.display('GO!  ')
            for racer in self.racers:
                racer.startRace()
                racer.setStartTime(startTime)
            self.display("Starttijd: " + datetime.datetime.fromtimestamp(time.time()).ctime())

        while (not self.status == State.RaceFinished) and (not self.exit):    
            time.sleep(1)
        self.display("Race gefinished, type een commando...")
