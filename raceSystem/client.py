import socket
import time
import configparser
import subprocess
import readline  # noqa: F401 This import is magically used, it enabled command line history
from _thread import start_new_thread
try:
    import RPi.GPIO as GPIO  # type: ignore
    testMode = False
except ModuleNotFoundError:
    testMode = True


class Client:
    def __init__(self, clientName, GPIOP1, GPIOP2, serverIP):
        self._clientName = clientName
        self._connected = False
        self._p1time = None
        self._p2time = None
        if testMode:
            self._serverIp = socket.gethostname()  # as both code is running on same pc
        else:
            self._serverIp = serverIP
            self.setupGPIO(GPIOP1, GPIOP2)

    def setupGPIO(self, GPIOP1, GPIOP2):
        # Switch pinmode to Broadcom SOC and disable warnings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # set GPIO pins as input
        GPIO.setup(GPIOP1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIOP2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Use interrupt, when active run 'signalFoundP<player>'
        GPIO.add_event_detect(GPIOP1, GPIO.RISING, callback=self.signalFoundP1, bouncetime=200)
        GPIO.add_event_detect(GPIOP2, GPIO.RISING, callback=self.signalFoundP2, bouncetime=200)

    def signalFoundP1(self, pin):
        if self._p1time is None:
            self._p1time = self.getCurrentMilliTime()
        print("GPIO{} pressed".format(pin))

    def signalFoundP2(self, pin):
        if self._p2time is None:
            self._p2time = self.getCurrentMilliTime()
        print("GPIO{} pressed".format(pin))

    def getCurrentMilliTime(self):
        return str(round(time.time() * 1000))

    def createSocket(self):
        port = 5000  # socket server port number
        clientSocket = socket.socket()  # instantiate
        clientSocket.connect((self._serverIp, port))  # connect to the server
        return clientSocket

    def connectToServer(self):
        while not self._connected:
            try:
                print("Trying to connect")
                clientSocket = self.createSocket()
                self._connected = True
                print("Connected")
            except ConnectionRefusedError:
                time.sleep(1)  # Wait 1 sec and try again
        return clientSocket

    def getInput(self):
        while self._connected:
            userInput = input("Enter 1 of 2 om voor p1 of p2 een sensor signaal te simuleren...")
            if userInput == '1':
                self.signalFoundP1(0)
            if userInput == '2':
                self.signalFoundP2(0)
            userInput = ''

    def sendMessage(self, clientSocket, message):
        try:
            clientSocket.send(message.encode())  # send message
            _ = clientSocket.recv(1024).decode()  # receive response
        except BrokenPipeError:
            print('Lost connection')
            self._connected = False

    def heartBeat(self, clientSocket):
        while self._connected:
            message = "Beat" + self._clientName
            self.sendMessage(clientSocket, message)
            time.sleep(0.5)

    def runClientProgram(self):
        while True:
            if not self._connected:
                clientSocket = self.connectToServer()
                identificationMessageToServer = self._clientName
                self.sendMessage(clientSocket, identificationMessageToServer)
                start_new_thread(self.heartBeat, (clientSocket,))
                if testMode:
                    start_new_thread(self.getInput, ())

            while self._connected:
                time.sleep(0.01)  # for CPU optimization
                if self._p1time is not None:
                    message = "p1" + self._clientName + ":" + self._p1time
                    self.sendMessage(clientSocket, message)
                    self._p1time = None
                if self._p2time is not None:
                    message = "p2" + self._clientName + ":" + self._p2time
                    self.sendMessage(clientSocket, message)
                    self._p2time = None

        clientSocket.close()  # close the connection


def readClientConfig():
    config = configparser.ConfigParser()
    config.read_file(open(r'client_config.txt'))
    if config.get('Client', 'client_type') == 'start':
        clientName = "StartClient"
    elif config.get('Client', 'client_type') == 'finish':
        clientName = "FinishClient"
    else:
        print("client_type in client_config file moet start of finish zijn")
        quit()
    GPIOP1 = int(config.get('Client', 'gpio_in_p1'))
    GPIOP2 = int(config.get('Client', 'gpio_in_p2'))
    serverIp = config.get('Client', 'server_ip')
    return clientName, GPIOP1, GPIOP2, serverIp


def enablePtpTimesync():
    timeSyncCommands = [
        "sudo systemctl stop systemd-timesyncd",
        "sudo systemctl disable systemd-timesyncd",
        "sudo iwconfig wlan0 power off",
        "sudo ptpd -s wlan0"]

    for command in timeSyncCommands:
        subprocess.run(command.split())


if __name__ == '__main__':
    if not testMode:
        enablePtpTimesync()
    clientName, GPIOP1, GPIOP2, serverIp = readClientConfig()
    print("Starting %s" % (clientName))
    client = Client(clientName, GPIOP1, GPIOP2, serverIp)
    client.runClientProgram()
