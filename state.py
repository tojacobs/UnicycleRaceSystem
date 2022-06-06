import enum

class State(enum.Enum):
    NotReadyToRace = -1
    ReadyToRace = 0
    CountdownFase1 = 10
    CountdownFase2 = 20
    RaceStarted = 100
    RaceFinished = 200
    RaceCanceled = 999
