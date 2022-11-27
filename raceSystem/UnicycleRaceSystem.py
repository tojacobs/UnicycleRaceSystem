from raceSystem.server import Server
from raceSystem.raceSequence import RaceSequence
from raceSystem.terminalUI import TerminalUI
from raceSystem.trafficLight import testMode
from _thread import start_new_thread


class UnicycleRaceSystem:
    def __init__(self):
        self._UIs = []
        self._raceSequence = RaceSequence()
        self._server = Server()
        self._UIs.append(TerminalUI())

    def exit(self):
        self._raceSequence.exit()
        self._server.exit()
        for ui in self._UIs:
            ui.exit()

    def receivedDataFromServer(self, data):
        self._raceSequence.processReceivedData(data)

    def startRace(self):
        self._raceSequence.startRace()

    def stopRace(self):
        self._raceSequence.stopRace()

    def setName(self, index, name):
        self._raceSequence.setName(index, name)

    def getName(self, index):
        return self._raceSequence.getName(index)

    def setCountdown(self, seconds):
        self._raceSequence.setCountdown(seconds)

    def getCountdown(self):
        return self._raceSequence.getCountdown()

    def setOrangeLightAt(self, seconds):
        self._raceSequence.setOrangeLightAt(seconds)

    def getOrangeLightAt(self):
        return self._raceSequence.getOrangeLightAt()

    def setResetTimerSeconds(self, seconds):
        self._raceSequence.setResetTimerSeconds(seconds)

    def getResetTimerSeconds(self):
        return self._raceSequence.getResetTimerSeconds()

    def startClientConnected(self):
        for ui in self._UIs:
            ui.startClientConnected()

    def finishClientConnected(self):
        for ui in self._UIs:
            ui.finishClientConnected()

    def startClientLost(self):
        for ui in self._UIs:
            ui.startClientLost()

    def finishClientLost(self):
        for ui in self._UIs:
            ui.finishClientLost()

    def countDownStarted(self):
        for ui in self._UIs:
            ui.countDownStarted()

    def countDownEnded(self):
        for ui in self._UIs:
            ui.countDownEnded()

    def raceEnded(self, winner):
        for ui in self._UIs:
            ui.raceEnded(winner)

    def sendResult(self, index, falseStart, DNF, raceTime, reactionTimeMs):
        for ui in self._UIs:
            ui.sendResult(index, falseStart, DNF, raceTime, reactionTimeMs)

    def startSignalDetected(self, index):
        for ui in self._UIs:
            ui.startSignalDetected(index)

    def finishSignalDetected(self, index):
        for ui in self._UIs:
            ui.finishSignalDetected(index)

    def falseStartDetected(self, index):
        for ui in self._UIs:
            ui.falseStartDetected(index)

    def run(self):
        self._raceSequence.setCallbackFunctions(self.countDownStarted, self.countDownEnded, self.raceEnded, self.sendResult,
                                                self.startSignalDetected, self.finishSignalDetected, self.falseStartDetected)
        self._server.setCallbackFunctions(self.receivedDataFromServer, self.startClientConnected, self.finishClientConnected,
                                          self.startClientLost, self.finishClientLost)
        for ui in self._UIs:
            ui.setCallbackFunctions(self.exit, self.startRace, self.stopRace, self.setName, self.getName,
                                    self.setCountdown, self.getCountdown, self.setOrangeLightAt, self.getOrangeLightAt,
                                    self.setResetTimerSeconds, self.getResetTimerSeconds)

        for ui in self._UIs:
            start_new_thread(ui.run, ())

        if testMode:
            start_new_thread(self._server.run, ())
            self._raceSequence.keepUpdatingTrafficlight()
        else:
            self._server.run()


if __name__ == '__main__':
    raceSystem = UnicycleRaceSystem()
    raceSystem.run()
