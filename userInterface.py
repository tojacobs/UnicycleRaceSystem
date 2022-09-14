class UserInterface:
    def __init__(self) -> None:
        pass
    def start(self):
        pass
    def exit(self):
        pass
    def setCallbackFunctions(self, exitCallback, startRaceCallback, stopRaceCallback, setNameCallback, getNameCallback,
                             setCountdownCallback, getCountdownCallback, setOrangeLightAtCallback, getOrangeLightAtCallback):
        pass
    def startClientConnected(self):
        pass 
    def finishClientConnected(self):
        pass
    def startClientLost(self):
        pass
    def finishClientLost(self):
        pass
    def countDownStarted(self):
        pass
    def countDownEnded(self):
        pass
    def raceEnded(self):
        pass
    def sendResult(self, index:int, finished:bool, falseStart:bool, DNF:bool, raceTime:tuple):
        pass
