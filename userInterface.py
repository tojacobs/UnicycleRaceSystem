from raceSequence import RaceSequence
from server import Server


class UserInterface:
    def __init__(self,raceSequence:RaceSequence) -> None:
        pass
    def start(self):
        pass
    def exit(self):
        pass
    def displayText(self, text:str, end:str):
        pass
    def setCallbackFunctions(self, exitCallback, startRaceCallback, stopRaceCallback):
        pass
    def startClientConnected(self):
        pass 
    def finishClientConnected(self):
        pass
    def startClientLost(self):
        pass
    def finishClientLostCallback(self):
        pass
