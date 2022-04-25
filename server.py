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
        while True:
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

    def countdown(self, t):
        orangeLightAt = t / 3
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
            if (t == orangeLightAt):
                for racer in self._racers:
                    if not (racer.getFalseStart()):
                        racer._light.turnOn(Color.Orange)

    def repairConnection(self, server_socket):
        conn, address = server_socket.accept()  # accept new connection
        start_new_thread(self.multi_threaded_client, (conn, address[1], ))

    def keepSteadyConnection(self):
        # get the hostname
        host = socket.gethostname()
        port = 5000  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many clients the server can listen simultaneously
        server_socket.listen(2)
        while True:
            if not self.bothClientsConnected():
                self.repairConnection(server_socket)

    def server_program(self):
        start_new_thread(self.keepSteadyConnection, ())

        while True:
            time.sleep(1)
            while not self.bothClientsConnected():
                print("Waiting for connection with clients")
                time.sleep(2)
            for racer in self._racers:
                racer.reset()
            print ("\nNieuwe race gestart!")
            self._status = State.WaitingForCountDown
            input("Drup op enter om de countdown te beginnen...\n")
            self._status = State.CountingDown
            self.countdown(3)
            if (not self._status == State.RaceFinished):
                self._status = State.RaceStarted
                startTime = time.time()
                print('GO!  ')
                for racer in self._racers:
                    racer.startRace()
                    racer.setStartTime(startTime)
                print("Starttijd: " + datetime.datetime.fromtimestamp(time.time()).ctime())

            while (not self._status == State.RaceFinished):
                time.sleep(1)
            input("Drup op enter om een nieuwe race te starten...\n")

        conn.close()  # close the connection


if __name__ == '__main__':
    server = Server()
    server.server_program()
