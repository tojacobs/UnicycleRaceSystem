import socket
from _thread import start_new_thread
import time
from raceSystem.trafficLight import testMode


class Server:
    def __init__(self):
        self._startClientConnected = False
        self._finishClientConnected = False
        self._startClientId = None
        self._finishClientId = None
        self._startLastHeartbeat = 0
        self._finishLastHeartbeat = 0
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

    def startConnectionLost(self):
        self._startClientConnected = False
        self.startClientLostCallback()

    def finishConnectionLost(self):
        self._finishClientConnected = False
        self.finishClientLostCallback()

    def recievedHeartBeat(self, data):
        if ("StartClient" in data):
            self._startLastHeartbeat = 0
        elif ("FinishClient" in data):
            self._finishLastHeartbeat = 0

    def watchDogHeartbeat(self):
        timeoutHeatbeat = 2
        while not self._exit:
            time.sleep(1)
            if self.bothClientsConnected():
                self._startLastHeartbeat = self._startLastHeartbeat + 1
                if self._startLastHeartbeat >= timeoutHeatbeat:
                    self._startLastHeartbeat = 0
                    self.startConnectionLost()
                self._finishLastHeartbeat = self._finishLastHeartbeat + 1
                if self._finishLastHeartbeat >= timeoutHeatbeat:
                    self._finishLastHeartbeat = 0
                    self.finishConnectionLost()
            else:
                self._startLastHeartbeat = 0
                self._finishLastHeartbeat = 0

    def multi_threaded_client(self, connection, id):
        while not self._exit:
            try:
                data = connection.recv(1024).decode()
                if not (self.bothClientsConnected()):
                    self.checkIfNewClient(str(data), id)
                if data.startswith("Beat"):
                    self.recievedHeartBeat(data)
                else:
                    self.receivedDataCallback(data)
                data = "Thanks for data"
                connection.send(data.encode())  # send Thanks for data to the client
            except BrokenPipeError:
                if (id == self._startClientId):
                    self.startConnectionLost()
                elif (id == self._finishClientId):
                    self.finishConnectionLost()
                break
        connection.close()

    def repairConnection(self, server_socket):
        conn, address = server_socket.accept()  # accept new connection
        start_new_thread(self.multi_threaded_client, (conn, address[1], ))

    def keepSteadyConnection(self):
        # get the hostname if testmode is active otherwise use real ip
        if testMode:
            host = socket.gethostname()
        else:
            host = "192.168.1.173"
        port = 5000  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        # Allow the socket to forcibly bind to a port in use by another socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many clients the server can listen simultaneously
        server_socket.listen(2)

        start_new_thread(self.watchDogHeartbeat, ())
        while not self._exit:
            time.sleep(0.1)  # for cpu usage optimization
            if not self.bothClientsConnected():
                self.repairConnection(server_socket)

    def run(self):
        self.keepSteadyConnection()
