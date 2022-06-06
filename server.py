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
        self._startClientConnected = False
        self._finishClientConnected = False
        self._startClientId = None
        self._finishClientId = None

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
            if not self.bothClientsConnected():
                self.repairConnection(server_socket)

    def waitForClients(self):
        # added an extra sleep because of port is still busy and enter is pushed twice fast this loop would start and program would be stuck
        time.sleep(0.1)
        while (not self.bothClientsConnected()) and (not self._answer == "exit"):
            print("Wacht op connectie met beide clients")
            time.sleep(2)

    
    def main(self):
        start_new_thread(self.keepSteadyConnection, ())


        self.waitForClients()
        if not self._answer == "exit":
            self.printHelp()

        while not self._answer == "exit":
            if not self._answer == "":
                self.processCommand()


if __name__ == '__main__':
    pass
