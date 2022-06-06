


from RaceSequence import RaceSequence
from server import Server
from UserInterface import UserInterface
from uiPython import uiPython
from _thread import *
from state import State




class MainProgram:
    UI:UserInterface
    server:Server
    raceSequence:RaceSequence

    def __init__(self):
        self.raceSequence = RaceSequence()
        self.server = Server()

        self.raceSequence.setState(State.ReadyToRace)
        self.UI = uiPython(self.raceSequence)

        




        
mainProgram:MainProgram

if __name__ == '__main__':
    main = MainProgram()
    start_new_thread(main.UI.main())

    main.server.main()