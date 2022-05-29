import socket
import os
from _thread import *
import time
import datetime
from state import State
from trafficLight import *
from Racer import Racer

class Server:
    def __init__(self):
        self._status = State.WaitingForCountDown
        self._startClientConnected = False
        self._finishClientConnected = False
        self._startClientId = None
        self._finishClientId = None
        self._racers = [Racer("P1", 1, 1, 1), Racer("P2", 2, 2, 2)]
        self._answer = ""
        self._countdown = 3
        self._orangeLightAt = 1

    def bothClientsConnected(self):
        return (self._startClientConnected and self._finishClientConnected)

    def checkIfNewClient(self, data, id):
        if ("StartClient" in data) and (not self._startClientConnected):
            self._startClientConnected = True
            self._startClientId = id
            print("StartClient Connected")
        elif ("FinishClient" in data) and (not self._finishClientConnected):
            self._finishClientConnected = True
            self._finishClientId = id
            print("FinishClient Connected")

    def endRaceIfNeeded(self):
        endRace = []
        for racer in self._racers:
            if (racer.getFinished() or racer.getFalseStart()):
                endRace.append(True)
            else:
                endRace.append(False)
        if all(endRace):
            self._status = State.RaceFinished

    def processFalseStart(self, data, racer):
        racer.setFalseStart(True)
        print(racer.printResult())
        self.endRaceIfNeeded()

    def processEndTime(self, data, racer):
        if not (racer.getFalseStart() or racer.getFinished()):
            data = data.split(':')[1]
            racer.setFinishTime(float(data)/1000)
            print(racer.printResult())
        self.endRaceIfNeeded()

    def processReceivedData(self, data):
        if self._status == State.CountingDown:
            if (data.startswith("p1StartClient")):
                self.processFalseStart(data, self._racers[0])
            elif (data.startswith("p2StartClient")):
                self.processFalseStart(data, self._racers[1])
        elif self._status == State.RaceStarted:
            if (data.startswith("p1FinishClient")):
                self.processEndTime(data, self._racers[0])
            elif (data.startswith("p2FinishClient")):
                self.processEndTime(data, self._racers[1])

    def multi_threaded_client(self, connection, id):
        while not self._answer == "exit":
            try:
                data = connection.recv(1024).decode()
                if not (self.bothClientsConnected()):
                    self.checkIfNewClient(str(data), id)
                self.processReceivedData(data)
                data = "Thanks for data"
                connection.send(data.encode())  # send Thanks for data to the client
            except:
                if (id == self._startClientId):
                    self._startClientConnected = False
                    print("Connectie met startClient verloren")
                elif (id == self._finishClientId):
                    self._finishClientConnected = False
                    print("Connectie met finishClient verloren")
                break
        connection.close()

    def startCountdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
            if (t == self._orangeLightAt):
                for racer in self._racers:
                    if not (racer.getFalseStart()):
                        racer._light.turnOn(Color.Orange)
                        racer._light.turnOff(Color.Red)

    def repairConnection(self, server_socket):
        conn, address = server_socket.accept()  # accept new connection
        start_new_thread(self.multi_threaded_client, (conn, address[1], ))

    def keepSteadyConnection(self):
        # get the hostname
        host = socket.gethostname()
        port = 5000  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #Allows the socket to forcibly bind to a port in use by another socket
        
        # try to execute bind function, if it fails shut down the program
        try:
            server_socket.bind((host, port))  # bind host address and port together
        except:
            print("Poort is nog bezet, wacht 1 a 2 minuten")
            self._answer = "exit"

        # configure how many clients the server can listen simultaneously
        server_socket.listen(2)
        while not self._answer == "exit":
            time.sleep(0.1) # for cpu usage optimization
            if not self.bothClientsConnected():
                self.repairConnection(server_socket)

    def waitForAnswer(self):
        while not self._answer == "exit":
            time.sleep(0.1)
            self._answer = input()

    def waitForClients(self):
        while (not self.bothClientsConnected()) and (not self._answer == "exit"):
            print("Wacht op connectie met beide clients")
            time.sleep(2)

    def startRace(self):
        self._status = State.WaitingForCountDown
        self.waitForClients()
        for racer in self._racers:
            racer.reset()
        print("\nNieuwe race gestart! Countdown is begonnen!")
        self._status = State.CountingDown
        self.startCountdown(self._countdown)
        if (not self._status == State.RaceFinished):
            self._status = State.RaceStarted
            startTime = time.time()
            print('GO!  ')
            for racer in self._racers:
                racer.startRace()
                racer.setStartTime(startTime)
            print("Starttijd: " + datetime.datetime.fromtimestamp(time.time()).ctime())

        while (not self._status == State.RaceFinished) and (not self._answer == "stop") and (not self._answer == 'exit'):    
            time.sleep(1)
        print("Race gefinished, type een commando...")

    def setNames(self):
        try:
            self._racers[0].setName(input("Geef naam van P1...\n"))
            print("{} Raced als P1".format(self._racers[0].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")
        try:
            self._racers[1].setName(input("Geef naam van P2...\n"))
            print("{} Raced als P2".format(self._racers[1].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")

    def setCountdown(self):
        try:
            self._countdown = int(input("Geef aantal seconden...\n"))
            print("countdown ingesteld op {} seconden".format(self._countdown))
        except:
            print("Ongeldig getal, instelling niet opgeslagen ")

    def setOrangeLightAt(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer <= self._countdown:
                self._orangeLightAt = answer
                print("Oranje licht ingesteld op {} seconden".format(self._orangeLightAt))
            else:
                print("Oranje licht sec mag niet hoger zijn dan countdown, instelling niet opgeslagen")
        except:
            print("Ongeldig getal, instelling niet opgeslagen")

    def processCommand(self):
        if self._answer == "start":
            self.startRace()
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

    def printHelp(self):
        print("Mogelijke commando's zijn: \n-'start' Om de countdown te beginnen.\n-'namen' Om namen van Racers in te geven.\n-'countdown' Om aantal sec countdown in te stellen.\n-'oranje' Om aantal sec vóór einde countdown in te stellen waarbij het oranje licht aangaat, default is 1.\n-'stop' Om de race af te breken, alleen te gebruiken tijdens de race.\n-'help' Om dit bericht te printen")

    def server_program(self):
        start_new_thread(self.keepSteadyConnection, ())
        start_new_thread(self.waitForAnswer, ())

        self.waitForClients()
        if not self._answer == "exit":
            self.printHelp()

        while not self._answer == "exit":
            time.sleep(0.1) # for cpu usage optimization
            if not self._answer == "":
                self.processCommand()


if __name__ == '__main__':
    server = Server()
    server.server_program()
