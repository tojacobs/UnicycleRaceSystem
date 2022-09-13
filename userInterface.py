from raceSequence import RaceSequence
from server import Server


class UserInterface:
    def __init__(self,raceSequence:RaceSequence) -> None:
        pass
    def displayText(self, text:str, end:str):
        pass
    def start(self):
        pass
    def setExitCommandCallback(self, Callback):
        pass
    def startClientConnected(self):
        pass 
    def finishClientConnected(self):
        pass
    def startClientLost(self):
        pass
    def finishClientLostCallback(self):
        pass
