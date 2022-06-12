import socket
import os
from _thread import *
import time
import datetime
from raceSequence import *

class Server:
    def __init__(self):
        self._startClientConnected = False
        self._finishClientConnected = False
        self._startClientId = None
        self._finishClientId = None
        self._answer = ""
        self._raceSequence = RaceSequence()
  
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

    def multi_threaded_client(self, connection, id):
        while not self._answer == "exit":
            try:
                data = connection.recv(1024).decode()
                if not (self.bothClientsConnected()):
                    self.checkIfNewClient(str(data), id)
                self._raceSequence.processReceivedData(data)
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

    def repairConnection(self, server_socket):
        conn, address = server_socket.accept()  # accept new connection
        start_new_thread(self.multi_threaded_client, (conn, address[1], ))

    def keepSteadyConnection(self):
        # get the hostname if testmode is active otherwise use real ip
        # Todo: implement a proper way to get testMode from trafficlight, currently it works because we import everything from raceSequence
        # which imports everything from trafficLight and testMode is a global in trafficLight
        if testMode:
            host = socket.gethostname()
        else:
            host = "192.168.1.173"
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

    def setNames(self):
        try:
            self._raceSequence.racers[0].setName(input("Geef naam van P1...\n"))
            print("{} Raced als P1".format(self._raceSequence.racers[0].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")
        try:
            self._raceSequence.racers[1].setName(input("Geef naam van P2...\n"))
            print("{} Raced als P2".format(self._raceSequence.racers[1].getName()))
        except:
            print("Ongeldige naam, instelling niet opgeslagen")

    def setCountdown(self):
        try:
            self._raceSequence.countdown = int(input("Geef aantal seconden...\n"))
            print("countdown ingesteld op {} seconden".format(self._raceSequence.countdown))
        except:
            print("Ongeldig getal, instelling niet opgeslagen ")

    def setOrangeLightAt(self):
        try:
            answer = int(input("Geef aantal seconden...\n"))
            if answer <= self._raceSequence.countdown:
                self._raceSequence.orangeLightAt = answer
                print("Oranje licht ingesteld op {} seconden".format(self._raceSequence.orangeLightAt))
            else:
                print("Oranje licht sec mag niet hoger zijn dan countdown, instelling niet opgeslagen")
        except:
            print("Ongeldig getal, instelling niet opgeslagen")

    def processCommand(self):
        if self._answer == "start":
            self.waitForClients()
            if (not self._answer == 'exit'):
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

        self._raceSequence.stop = True


if __name__ == '__main__':
    server = Server()
    server.server_program()
