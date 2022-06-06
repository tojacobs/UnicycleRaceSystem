import datetime
from xmlrpc.client import Boolean, boolean
from state import State
import time
from Racer import Racer
from trafficLight import *


class RaceSequence:
    def __init__(self):
        self.racers = {Racer('P1'),Racer('P2')}
        self.lights = {TrafficLight(1,1,1),TrafficLight(2,2,2)}
        self._countdown = 3
        self._orangeLightAt = 1
        self._state = State.NotReadyToRace
        self._onStateChanged = None

    def endRaceIfNeeded(self):
        endRace = []
        for racer in self.racers:
            if (racer.getFinished() or racer.getFalseStart()):
                endRace.append(True)
            else:
                endRace.append(False)
        if all(endRace):
            self._state = State.RaceFinished

    def setReadyToRace(self, ready):
        if ready:
            if self._state == State.NotReadyToRace:
                self.setState(State.ReadyToRace)
        else:
            self.setState(State.NotReadyToRace)

    def setCountdown(self, countdown) -> Boolean:
        accepted = countdown > self._orangeLightAt
        if (accepted):
            self._countdown = countdown    
        return accepted

    def setOrangeLightAt(self, orangeLightAt) -> Boolean:
        accepted = orangeLightAt < self._countdown
        if (accepted):
            self._orangeLightAt = orangeLightAt
        return accepted

    def setOnStateChanged(self,func):
        self._onStateChanged = func

    def setState(self,state):
        if self._state != state and self._onStateChanged != None:
            self._onStateChanged()
        self._state = state
    
    def getCountdown(self):
        return self._countdown

    def getOrangeLightAt(self):
        return self._orangeLightAt

    def getState(self):
        return self._state

    def cancelRace(self):
        if (not self._state == State.NotReadyToRace):
            self._state = State.ReadyToRace
            print("Race is gecanceld")

    def startlineDetected(self, track:int, time):
        if self._state >= State.CountdownFase1 and self._state < State.RaceFinished:
            self.racers[track].setStartLineTime(time)

    def finschlineDetected(self, track, time):
        if self._state >= State.RaceStarted and self._state < State.RaceFinished:
            self.racers[track].setFinishTime(time)

    def processFalseStart(self, racer):
        racer.setFalseStart(True)
        print(racer.printResult())
        self.endRaceIfNeeded()

    def processEndTime(self, data, racer):
        if not (racer.getFalseStart() or racer.getFinished()):
            data = data.split(':')[1]
            racer.setFinishTime(float(data)/1000)
            print(racer.printResult())
        self.endRaceIfNeeded()

    def startRace(self):
        if (self._state != State.ReadyToRace):
            print('Not ready to race')
            return

        for racer in self.racers:
            racer.reset()

        self.setState(State.CountdownFase1)

        for light in self.lights:
            light.turnOn(Color.Red)
            light.turnOff(Color.Orange)
            light.turnOff(Color.Green)

        t = self._countdown
        while t and self._state != State.NotReadyToRace:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
            if (t == self._orangeLightAt):
                self.setState(State.CountdownFase2)

                for light in self.lights:
                    light.turnOff(Color.Red)
                    light.turnOn(Color.Orange)
                    light.turnOff(Color.Green)

        for light in self.lights:
                    light.turnOff(Color.Red)
                    light.turnOff(Color.Orange)
                    light.turnOn(Color.Green)

        if (self._state == State.NotReadyToRace):
            return
        else:
            self.setState(State.RaceStarted)

        startTime = time.time()
        print('GO!  ')
        for racer in self.racers:
            racer.setStartTime(startTime)
        print("Starttijd: " + datetime.datetime.fromtimestamp(startTime).ctime())

        RaceOver = []
        while not all(RaceOver) and self._state == State.RaceStarted:
            for racer in self.racers:
                RaceOver.append(racer.RaceIsOver())
            time.sleep(0.1)

        if (self._state == State.NotReadyToRace):
            return
        else:
            self.setState(State.RaceFinished)
print("Race gefinished, type een commando...")