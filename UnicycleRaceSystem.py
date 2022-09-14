from server import Server
from raceSequence import RaceSequence
from terminalUI import TerminalUI
from userInterface import UserInterface
from _thread import *

class UnicycleRaceSystem:
    def __init__(self):
        self._raceSequence = RaceSequence()
        self._server = Server()
        self._UserInterface = TerminalUI(self._raceSequence)

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

    def run(self):
        self._raceSequence.setCallbackFunctions(self.display)
        self._server.setCallbackFunctions(self.receivedDataFromServer, self.startClientConnected, self.finishClientConnected, 
                                          self.startClientLost, self.finishClientLostCallback)
        self._UserInterface.setCallbackFunctions(self.exit, self.startRace, self.stopRace)

        start_new_thread(self._server.server_program,())
        self._UserInterface.start()

if __name__ == '__main__':
    raceSystem = UnicycleRaceSystem()
    raceSystem.run()
    
