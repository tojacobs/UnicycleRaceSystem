from server import Server
from raceSequence import RaceSequence

class UnicycleRaceSystem:
    def __init__(self):
        self._raceSequence = RaceSequence()
        self._server = Server(self._raceSequence)

    def receivedDataFromServer(self, data):
        self._raceSequence.processReceivedData(data)

    def display(self, data, end = "\n"):
        # Todo: after UI is split off let send this data to UI
        print(data, end=end)

    def run(self):
        self._raceSequence.setCallbackFunctions(self.display)
        self._server.setCallbackFunctions(self.receivedDataFromServer, self.display)
        self._server.server_program()

if __name__ == '__main__':
    raceSystem = UnicycleRaceSystem()
    raceSystem.run()
    
