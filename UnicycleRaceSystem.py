from server import Server
from raceSequence import RaceSequence
from terminalUI import TerminalUI
from _thread import *

class UnicycleRaceSystem:
    def __init__(self):
        self._raceSequence = RaceSequence()
        self._server = Server()
        self._UserInterface = TerminalUI()

    def receivedDataFromServer(self, data):
        self._raceSequence.processReceivedData(data)

    def display(self, data, end = "\n"):
        self._UserInterface.displayText(data, end)

    def startClientConnected(self):
        self._UserInterface.startClientConnected()

    def finishClientConnected(self):
        self._UserInterface.finishClientConnected()

    def startClientLost(self):
        self._UserInterface.startClientLost()

    def finishClientLostCallback(self):
        self._UserInterface.finishClientLostCallback()

    def exit(self):
        self._raceSequence.exit()
        self._server.exit()
        self._UserInterface.exit()

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

    def run(self):
        self._raceSequence.setCallbackFunctions(self.display)
        self._server.setCallbackFunctions(self.receivedDataFromServer, self.startClientConnected, self.finishClientConnected, 
                                          self.startClientLost, self.finishClientLostCallback)
        self._UserInterface.setCallbackFunctions(self.exit, self.startRace, self.stopRace, self.setName, self.getName,
                                                 self.setCountdown, self.getCountdown, self.setOrangeLightAt, self.getOrangeLightAt)

        start_new_thread(self._server.server_program,())
        self._UserInterface.start()

if __name__ == '__main__':
    raceSystem = UnicycleRaceSystem()
    raceSystem.run()
    
