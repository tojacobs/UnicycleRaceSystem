import enum

class State(enum.Enum):
    WaitingForCountDown = 1 
    CountingDown = 2
    RaceStarted = 3
    RaceFinished = 4
