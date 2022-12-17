import abc


class UserInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        """Initialization"""
        pass

    @abc.abstractmethod
    def run(self):
        """Start the user interface"""
        pass

    @abc.abstractmethod
    def setCallbackFunctions(self, exitCallback, startRaceCallback, stopRaceCallback, setNameCallback, getNameCallback,
                             setCountdownCallback, getCountdownCallback, setOrangeLightAtCallback, getOrangeLightAtCallback,
                             setResetTimerSeconds, getResetTimerSeconds):
        """setCallbackFunctions sets the callback functions that are being used by the user interface"""
        pass

    @abc.abstractmethod
    def exit(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def startClientConnected(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def finishClientConnected(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def startClientLost(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def finishClientLost(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def countDownStarted(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def countDownEnded(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def raceEnded(self, winner):
        """Callback function that will be called from UnicycleRaceSystem
        winner holds the name of the winner.
        If there is no winner, the value will be 'None'"""
        pass

    @abc.abstractmethod
    def sendResult(self, index: int, falseStart: bool, DNF: bool, raceTime: tuple, reactionTimeMs: int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def startSignalDetected(self, index: int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def finishSignalDetected(self, index: int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    @abc.abstractmethod
    def falseStartDetected(self, index):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
