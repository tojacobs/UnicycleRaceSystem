import imp
import time
from UserInterface import UserInterface
from RaceSequence import RaceSequence
from _thread import *


class uiPython(UserInterface):
    
    def __init__(self,raceSequence:RaceSequence):
        self._answer = ""
        self._raceSequence = raceSequence

    def setNames(self):
        try:
            self._raceSequence.racers[0].setName(input("Geef naam van P1...\n"))
            print("{} Raced als P1".format(self._racers[0].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")
        try:
            self._raceSequence._racers[1].setName(input("Geef naam van P2...\n"))
            print("{} Raced als P2".format(self._racers[1].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")

    def setCountdown(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer >= self._raceSequence.getOrangeLightAt():
                self._raceSequence.setCountdown(answer)
                print("countdown ingesteld op {} seconden".format(self._raceSequence.getCountdown())) 
            else:
                print("Countdown sec mag niet lager zijn dan oranje licht, instelling niet opgeslagen")  
        except:
            print("Ongeldig getal, instelling niet opgeslagen ")

    def setOrangeLightAt(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer <= self._raceSequence.getCountdown():
                self._raceSequence.setOrangeLightAt(answer)
                print("Oranje licht ingesteld op {} seconden".format(self._raceSequence.getOrangeLightAt()))
            else:
                print("Oranje licht sec mag niet hoger zijn dan countdown, instelling niet opgeslagen")
        except:
            print("Ongeldig getal, instelling niet opgeslagen")

    def waitForAnswer(self):
        while not self._answer == "exit":
            time.sleep(0.1)
            self._answer = input()

    def printHelp(self):
        print("Mogelijke commando's zijn: \n-'start' Om de countdown te beginnen.\n-'namen' Om namen van Racers in te geven.\n-'countdown' Om aantal sec countdown in te stellen.\n-'oranje' Om aantal sec vóór einde countdown in te stellen waarbij het oranje licht aangaat, default is 1.\n-'stop' Om de race af te breken, alleen te gebruiken tijdens de race.\n-'help' Om dit bericht te printen")

    def processCommand(self):
        if self._answer == "start":
            self._raceSequence.startRace()
        elif self._answer == "stop":
            self._raceSequence.cancelRace()
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
        else:
            print("type een geldig commando of type 'help'")
        self._answer = ""

    def main(self):
        start_new_thread(self.waitForAnswer, ())

        if not self._answer == "exit":
            self.printHelp()

        while not self._answer == "exit":
            if not self._answer == "":
                self.processCommand()   