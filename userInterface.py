class UserInterface:
    def __init__(self) -> None:
        """Initialization"""
        pass
    def run(self):
        """Start the user interface"""
        pass
    def setCallbackFunctions(self, exitCallback, startRaceCallback, stopRaceCallback, setNameCallback, getNameCallback,
                             setCountdownCallback, getCountdownCallback, setOrangeLightAtCallback, getOrangeLightAtCallback):
        """setCallbackFunctions sets the callback functions that are being used by the user interface"""
        pass
    def exit(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def startClientConnected(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass 
    def finishClientConnected(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def startClientLost(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def finishClientLost(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def countDownStarted(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def countDownEnded(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def raceEnded(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def sendResult(self, index:int, finished:bool, falseStart:bool, DNF:bool, raceTime:tuple):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
