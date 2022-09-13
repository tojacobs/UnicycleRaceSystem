from doctest import TestResults
import time
from Racer import Racer
from raceSequence import RaceSequence
from server import Server
from userInterface import UserInterface
from _thread import *


class TerminalUI(UserInterface):
    def __init__(self,server:Server,raceSequence:RaceSequence) -> None:
        self._server = server
        self._raceSequence = raceSequence
        self._answer = ""
        self._exit = False

    def exit(self):
        self._exit = True

    def displayText(self, text, end):
        print(text,end=end)

    def setExitCommandCallback(self, Callback):
        self.exitCallback = Callback

    def waitForAnswer(self):
        while not self._exit:
            time.sleep(0.1)
            self._answer = input()

    def setNames(self):
        try:
            self._raceSequence._racers[0].setName(input("Geef naam van P1...\n"))
            print("{} Raced als P1".format(self._raceSequence._racers[0].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")
        try:
            self._raceSequence._racers[1].setName(input("Geef naam van P2...\n"))
            print("{} Raced als P2".format(self._raceSequence._racers[1].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")

    def setCountdown(self):
        try:
            self._raceSequence._countdown = int(input("Geef aantal seconden...\n"))
            print("countdown ingesteld op {} seconden".format(self._raceSequence._countdown))
        except:
            print("Ongeldig getal, instelling niet opgeslagen ")

    def setOrangeLightAt(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer <= self._raceSequence._countdown:
                self._raceSequence._orangeLightAt = answer
                print("Oranje licht ingesteld op {} seconden".format(self._raceSequence._orangeLightAt))
            else:
                print("Oranje licht sec mag niet hoger zijn dan countdown, instelling niet opgeslagen")
        except:
            print("Ongeldig getal, instelling niet opgeslagen")

    def processCommand(self):
        if self._answer == "start":
            self._raceSequence.startRace()
        elif self._answer == "namen":
            self.setNames()
        elif self._answer == "countdown":
            self.setCountdown()
        elif self._answer == "oranje":
            self.setOrangeLightAt()
        elif self._answer == "help":
            self.printHelp()
        elif self._answer == "exit":
            print("poging tot programma afsluiten, mocht dit niet werken dan programma sluiten met Ctrl+c")
            self.exitCallback()
        else:
            print("type een geldig commando of type 'help'")
        self._answer = ""

    def printHelp(self):
        print("Mogelijke commando's zijn: \n-'start' Om de countdown te beginnen.\n-'namen' Om namen van Racers in te geven.\n-'countdown' Om aantal sec countdown in te stellen.\n-'oranje' Om aantal sec vóór einde countdown in te stellen waarbij het oranje licht aangaat.\n-'stop' Om de race af te breken, alleen te gebruiken tijdens de race.\n-'help' Om dit bericht te printen")

    def start(self):
        start_new_thread(self.waitForAnswer, ())

        while not self._server.bothClientsConnected() and not self._exit:
            if self._answer == "exit":
                self.exitCallback()
            time.sleep(0.1)
            
        if not self._exit:
            self.printHelp()
        while not self._exit:
            time.sleep(0.1) # for cpu usage optimization
            if not self._answer == "":
                self.processCommand()
