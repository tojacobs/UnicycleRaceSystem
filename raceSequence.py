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
        self.racers = [Racer("P1", 1, 1, 1), Racer("P2", 2, 2, 2)]
        self.stop = False

    def processEndTime(self, data, racer):
        if not (racer.getFalseStart() or racer.getFinished()):
            data = data.split(':')[1]
            racer.setFinishTime(float(data)/1000)
            print(racer.printResult())
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
        print(racer.printResult())
        self.endRaceIfNeeded()

    def startCountdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
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
        print("\nNieuwe race gestart! Countdown is begonnen!")
        self.status = State.CountingDown
        self.startCountdown(self.countdown)
        if (not self.status == State.RaceFinished):
            self.status = State.RaceStarted
            startTime = time.time()
            print('GO!  ')
            for racer in self.racers:
                racer.startRace()
                racer.setStartTime(startTime)
            print("Starttijd: " + datetime.datetime.fromtimestamp(time.time()).ctime())

        while (not self.status == State.RaceFinished) and (not self.stop):    
            time.sleep(1)
        print("Race gefinished, type een commando...")
