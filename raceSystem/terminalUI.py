import time
import readline  # noqa: F401 This import is magically used, it enabled command line history
from raceSystem.userInterface import UserInterface
from _thread import start_new_thread


class TerminalUI(UserInterface):
    def __init__(self) -> None:
        self._answer = ""
        self._exit = False
        self._startClientConnected = False
        self._finishClientConnected = False
        self._raceOngoing = False
        self._raceLengthInSec = 15

    def setCallbackFunctions(self, exitCallback, startRaceCallback, stopRaceCallback, setNameCallback, getNameCallback,
                             setCountdownCallback, getCountdownCallback, setOrangeLightAtCallback, getOrangeLightAtCallback,
                             setResetTimerSecondsCallback, getResetTimerSecondsCallback):
        self.exitCallback                 = exitCallback
        self.startRaceCallback            = startRaceCallback
        self.stopRaceCallback             = stopRaceCallback
        self.setNameCallback              = setNameCallback
        self.getNameCallback              = getNameCallback
        self.setCountdownCallback         = setCountdownCallback
        self.getCountdownCallback         = getCountdownCallback
        self.setOrangeLightAtCallback     = setOrangeLightAtCallback
        self.getOrangeLightAtCallback     = getOrangeLightAtCallback
        self.setResetTimerSecondsCallback = setResetTimerSecondsCallback
        self.getResetTimerSecondsCallback = getResetTimerSecondsCallback

    def exit(self):
        self._exit = True

    def startClientConnected(self):
        self._startClientConnected = True
        print("StartClient Connected")

    def finishClientConnected(self):
        self._finishClientConnected = True
        print("FinishClient Connected")

    def startClientLost(self):
        self._startClientConnected = False
        print("Connectie met StartClient verloren")

    def finishClientLost(self):
        self._finishClientConnected = False
        print("Connectie met FinishClient verloren")

    def countDownStarted(self):
        print("Nieuwe race gestart! Countdown is begonnen!")
        start_new_thread(self.startCountdown, (self.getCountdownCallback(), ))

    def countDownEnded(self):
        print("GO!  ")
        start_new_thread(self.startStopRaceTimer, (self._raceLengthInSec, ))

    def raceEnded(self, winner):
        print("Winnaar: %s" % winner)
        print("#########################################################################")
        print("Race gefinished, type een commando...")
        self._raceOngoing = False

    def sendResult(self, index, falseStart, DNF, raceTime, reactionTimeMs):
        if falseStart:
            if DNF:
                print("Resultaten %s: reactietijd: %s Ms,  Racetijd: DNF,  Valse start"
                      % (self.getNameCallback(index), reactionTimeMs))
            else:
                minutes, seconds = raceTime
                print("Resultaten %s: reactietijd: %s Ms,  Racetijd: %d:%.3f,  Valse start"
                      % (self.getNameCallback(index), reactionTimeMs, int(minutes), seconds))
        else:
            if DNF:
                print("Resultaten %s: reactietijd: %s Ms,  Racetijd: DNF"
                      % (self.getNameCallback(index), reactionTimeMs))
            else:
                minutes, seconds = raceTime
                print("Resultaten %s: reactietijd: %s Ms,  Racetijd: %d:%.3f"
                      % (self.getNameCallback(index), reactionTimeMs, int(minutes), seconds))

    def startSignalDetected(self, index):
        # print("Start sensor P%s gedetecteerd" % (index+1))
        pass

    def finishSignalDetected(self, index):
        # print("Finish sensor P%s gedetecteerd" % (index+1))
        pass

    def falseStartDetected(self, index):
        print("%s: Valse start gedetecteerd!" % (self.getNameCallback(index)))

    def startCountdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

    def startStopRaceTimer(self, t):
        while (t and self._raceOngoing):
            time.sleep(1)
            t -= 1
        if self._raceOngoing:
            print("Race wordt gestopt vanwege de maximale lengte van %s seconden" % self._raceLengthInSec)
            self.stopRaceCallback()

    def bothClientsConnected(self):
        return (self._startClientConnected and self._finishClientConnected)

    def waitForAnswer(self):
        while not self._exit:
            time.sleep(0.1)  # sleep is for CPU optimization
            self._answer = input()

    def setNames(self):
        try:
            self.setNameCallback(0, input("Geef naam van P1...\n"))
            print("{} Raced als P1".format(self.getNameCallback(0)))
        except SyntaxError:
            print("Ongeldige naam, instelling niet opgeslagen")
        try:
            p2name = input("Geef naam van P2...\n")
            if p2name != self.getNameCallback(0):
                self.setNameCallback(1, p2name)
                print("{} Raced als P2".format(self.getNameCallback(1)))
            else:
                print("Namen mogen niet hetzelfde zijn, instelling niet opgeslagen")
        except SyntaxError:
            print("Ongeldige naam, instelling niet opgeslagen")

    def setCountdown(self):
        try:
            # TODO countdown mag niet lager zijn dan orangeLightAt
            self.setCountdownCallback(int(input("Geef aantal seconden...\n")))
            print("countdown ingesteld op {} seconden".format(self.getCountdownCallback()))
        except ValueError:
            print("Ongeldig getal, instelling niet opgeslagen ")

    def setOrangeLightAt(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer <= self.getCountdownCallback():
                self.setOrangeLightAtCallback(answer)
                print("Oranje licht ingesteld op {} seconden".format(self.getOrangeLightAtCallback()))
            else:
                print("Oranje licht sec mag niet hoger zijn dan countdown, instelling niet opgeslagen")
        except ValueError:
            print("Ongeldig getal, instelling niet opgeslagen")

    def setMaxRaceLenght(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer > 0:
                self._raceLengthInSec = answer
                print("Maximale raceduur ingesteld op {} seconden".format(self._raceLengthInSec))
            else:
                print("Maximale raceduur mag niet negatief zijn")
        except ValueError:
            print("Ongeldig getal, instelling niet opgeslagen")

    def setWinnerIndicationTimer(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer > 0:
                self.setResetTimerSecondsCallback(answer)
                print("Stoplicht winnaar indicatie tijd ingesteld op {} seconden".format(self.getResetTimerSecondsCallback()))
            else:
                print("Stoplicht winnaar indicatie tijd mag niet negatief zijn")
        except ValueError:
            print("Ongeldig getal, instelling niet opgeslagen")

    def processCommand(self):  # noqa: C901 complexity for this function is too high but in this case it's ok.
        if self._raceOngoing and self._answer in {"start", "namen", "countdown", "oranje", "raceduur", "indicatie"}:
            print("De race is al begonnen, u kunt dit commando nu niet gebruiken")
        elif self._answer == "start":
            self._raceOngoing = True
            start_new_thread(self.startRaceCallback, ())
        elif self._answer == "namen":
            self.setNames()
        elif self._answer == "countdown":
            self.setCountdown()
        elif self._answer == "oranje":
            self.setOrangeLightAt()
        elif self._answer == "raceduur":
            self.setMaxRaceLenght()
        elif self._answer == "indicatie":
            self.setWinnerIndicationTimer()
        elif self._answer == "help":
            self.printHelp()
        elif self._answer == "stop":
            self.stopRaceCallback()
        elif self._answer == "exit":
            print("Programma afsluiten... mocht dit niet werken dan programma sluiten met Ctrl+c")
            self.exitCallback()
        else:
            print("type een geldig commando of type 'help'")
        self._answer = ""

    def printHelp(self):
        print("Mogelijke commando's zijn: \n\
-'start' Om de countdown te beginnen.\n\
-'namen' Om namen van Racers in te geven.\n\
-'countdown' Om aantal sec countdown in te stellen, default is 4 sec.\n\
-'oranje' Om aantal sec vóór einde countdown in te stellen waarbij het oranje licht aangaat, default is 2 sec.\n\
-'stop' Om de race af te breken, alleen te gebruiken tijdens de race.\n\
-'raceduur' Om de maximale raceduur in te stellen, racers krijgen een DNF na deze tijd, default is 15 sec.\n\
-'indicatie' Om aantal seconden van de winnaar indicatie op het stoplicht in te stellen, default is 30 sec.\n\
-'exit' Om het programma te sluiten.\n\
-'help' Om dit bericht te printen")

    def run(self):
        start_new_thread(self.waitForAnswer, ())
        helpPrinted = False

        while not self._exit:

            while not self.bothClientsConnected() and not self._exit:
                if self._answer == "exit":
                    self.exitCallback()
                if self._answer == "stop":
                    self.stopRaceCallback()
                if self._startClientConnected:
                    print("Wacht op connectie met finish client")
                elif self._finishClientConnected:
                    print("Wacht op connectie met start client")
                else:
                    print("Wacht op connectie met beide clients")
                time.sleep(2)

            if not helpPrinted:
                self.printHelp()
                helpPrinted = True

            time.sleep(0.1)  # for cpu usage optimization
            if not self._answer == "":
                self.processCommand()
