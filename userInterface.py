class UserInterface:
    def __init__(self) -> None:
        pass
    def start(self):
        pass
    def exit(self):
        pass
    def displayText(self, text:str, end:str):
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
    def finishClientLostCallback(self):
        pass
