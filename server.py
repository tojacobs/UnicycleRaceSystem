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
        self._exit = False

    def setCallbackFunctions(self, receivedDataCallback, startClientConnectedCallback, 
                             finishClientConnectedCallback, startClientLostCallback, finishClientLostCallback):
        """setCallbackFunctions sets the callback functions that are being used by server"""
        self.receivedDataCallback          = receivedDataCallback
        self.startClientConnectedCallback  = startClientConnectedCallback
        self.finishClientConnectedCallback = finishClientConnectedCallback
        self.startClientLostCallback       = startClientLostCallback
        self.finishClientLostCallback      = finishClientLostCallback

    def exit(self):
        """exit is a callback function that will be called from UnicycleRaceSystem"""
        self._exit = True

    def bothClientsConnected(self):
        return (self._startClientConnected and self._finishClientConnected)

    def checkIfNewClient(self, data, id):
        if ("StartClient" in data) and (not self._startClientConnected):
            self._startClientConnected = True
            self._startClientId = id
            self.startClientConnectedCallback()
        elif ("FinishClient" in data) and (not self._finishClientConnected):
            self._finishClientConnected = True
            self._finishClientId = id
            self.finishClientConnectedCallback()

    def multi_threaded_client(self, connection, id):
        while not self._exit:
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
                    self.startClientLostCallback()
                elif (id == self._finishClientId):
                    self._finishClientConnected = False
                    self.finishClientLostCallback()
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
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many clients the server can listen simultaneously
        server_socket.listen(2)
        while not self._exit:
            time.sleep(0.1) # for cpu usage optimization
            if not self.bothClientsConnected():
                self.repairConnection(server_socket)

    def run(self):
        self.keepSteadyConnection()

