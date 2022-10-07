import socket
import time
import configparser
try:
    import RPi.GPIO as GPIO
    testMode = False
except:
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
        # Zet de pinmode op Broadcom SOC.
        GPIO.setmode(GPIO.BCM)
        # Zet waarschuwingen uit.
        GPIO.setwarnings(False)
        # Zet de GPIO pin als ingang.
        GPIO.setup(GPIOP1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIOP2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Gebruik een interrupt, wanneer actief run subroutinne 'signal_found_p<player>'
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
            except:
                time.sleep(1) # Wait 1 sec and try again
        return clientSocket

    def getInput(self):
        return input("Enter 1 of 2 om voor p1 of p2 een sensor signaal te simuleren...")

    def sendMessage(self, clientSocket, message):
        try:
            clientSocket.send(message.encode())  # send message
            data = clientSocket.recv(1024).decode()  # receive response
        except:
            self._connected = False

    def runClientProgram(self):
        while True:
            if not self._connected:
                clientSocket = self.connectToServer()
                identificationMessageToServer = self._clientName
                self.sendMessage(clientSocket, identificationMessageToServer)

            while self._connected:
                if testMode:
                    racer = self.getInput()
                    message = "p" + racer + self._clientName + ":" + self.getCurrentMilliTime()
                    self.sendMessage(clientSocket, message)
                else:
                    time.sleep(0.01) # for CPU optimization
                    if not self._p1time is None:
                        message = "p1" + self._clientName + ":" + self._p1time
                        self.sendMessage(clientSocket, message)
                        self._p1time = None
                    if not self._p2time is None:
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

if __name__ == '__main__':
    clientName, GPIOP1, GPIOP2, serverIp = readClientConfig()
    print("Starting %s" % (clientName))
    client = Client(clientName, GPIOP1, GPIOP2, serverIp)
    client.runClientProgram()
