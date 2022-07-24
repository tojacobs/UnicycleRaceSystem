import socket
import os
from _thread import *
import time
import datetime
from raceSequence import *

class Server:
    def __init__(self, raceSequence):
        self._startClientConnected = False
        self._finishClientConnected = False
        self._startClientId = None
        self._finishClientId = None
        self._raceSequence = raceSequence
        self.exit = False

    def setCallbackFunctions(self, receivedDataCallback, displayCallback):
        self.receivedDataCallback = receivedDataCallback
        self.display = displayCallback

    def bothClientsConnected(self):
        return (self._startClientConnected and self._finishClientConnected)

    def checkIfNewClient(self, data, id):
        if ("StartClient" in data) and (not self._startClientConnected):
            self._startClientConnected = True
            self._startClientId = id
            self.display("StartClient Connected")
        elif ("FinishClient" in data) and (not self._finishClientConnected):
            self._finishClientConnected = True
            self._finishClientId = id
            self.display("FinishClient Connected")

    def multi_threaded_client(self, connection, id):
        while not self.exit:
            try:
                data = connection.recv(1024).decode()
                if not (self.bothClientsConnected()):
                    self.checkIfNewClient(str(data), id)
                self.receivedDataCallback(data)
                data = "Thanks for data"
                connection.send(data.encode())  # send Thanks for data to the client
            except:
                if (id == self._startClientId):
                    self._startClientConnected = False
                    self.display("Connectie met startClient verloren")
                elif (id == self._finishClientId):
                    self._finishClientConnected = False
                    self.display("Connectie met finishClient verloren")
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
            self.display("Poort is nog bezet, wacht 1 a 2 minuten")
            self.exit = True

        # configure how many clients the server can listen simultaneously
        server_socket.listen(2)
        while not self.exit:
            time.sleep(0.1) # for cpu usage optimization
            if not self.bothClientsConnected():
                self.repairConnection(server_socket)

    def waitForClients(self):
        while (not self.bothClientsConnected()) and (not self.exit):
            self.display("Wacht op connectie met beide clients")
            time.sleep(2)

    def server_program(self):
        start_new_thread(self.keepSteadyConnection, ())

        self.waitForClients()

        while not self.exit:
            time.sleep(0.1) # for cpu usage optimization

        
