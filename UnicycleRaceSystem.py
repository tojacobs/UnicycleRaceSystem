from server import Server
from raceSequence import RaceSequence
from terminalUI import TerminalUI
from userInterface import UserInterface
from _thread import *

class UnicycleRaceSystem:
    def __init__(self):
        self._raceSequence = RaceSequence()
        self._server = Server(self._raceSequence)
        self._UserInterface = TerminalUI(self._server, self._raceSequence)

    def receivedDataFromServer(self, data):
        self._raceSequence.processReceivedData(data)

    def display(self, data, end = "\n"):
        # Todo: after UI is split off let send this data to UI
        #print(data, end=end)
        self._UserInterface.displayText(data)

    def exit(self):
        self._raceSequence.exit = True
        self._server.exit = True
        self._UserInterface.exit = True

    def run(self):
        self._raceSequence.setCallbackFunctions(self.display)
        self._server.setCallbackFunctions(self.receivedDataFromServer, self.display)
        self._UserInterface.setExitCommandCallback(self.exit)

        start_new_thread(self._server.server_program,())
        self._UserInterface.start()

if __name__ == '__main__':
    raceSystem = UnicycleRaceSystem()
    raceSystem.run()
    
