import enum

class State(enum.Enum):
    ConnectingToClients = 1
    WaitingForCountDown = 2 
    CountingDown = 3
    RaceStarted = 4
    RaceFinished = 5
