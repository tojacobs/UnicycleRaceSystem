import socket
import time
import RPi.GPIO as GPIO
import time

def current_milli_time():
    return str(round(time.time() * 1000))

def connectToServer(host, port):
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    return client_socket

def singal_found_p1(pin):
    global p1time 
    print("GPIO{} pressed".format(pin))
    if p1time is None:
        p1time = current_milli_time()

def singal_found_p2(pin):
    global p2time 
    print("GPIO{} pressed".format(pin))
    if p2time is None:
        p2time = current_milli_time()

def client_program():
    global connected, p2time, p1time
    p1time = p2time = None
    connected = False
    host = "192.168.178.65"  # Fill in server's ip adress
    port = 5000  # socket server port number
    connected = False

    clientName = "StartClient"
    message = clientName

    while True:

        while not connected:
            try:
                time.sleep(1)
                print("Trying to connect")
                client_socket = connectToServer(host, port)
                connected = True
            except:
                pass

        try:
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response
        except:
            connected = False

        while connected:
            if not p1time is None:
                message = "p1" + clientName + ":" + p1time  # again take input
                try:
                    client_socket.send(message.encode())  # send message
                    data = client_socket.recv(1024).decode()  # receive response
                    p1time = None
                except:
                    connected = False
            if not p2time is None:
                message = "p2" + clientName + ":" + p2time  # again take input
                try:
                    client_socket.send(message.encode())  # send message
                    data = client_socket.recv(1024).decode()  # receive response
                    p2time = None
                except:
                    connected = False
            #print('Received from server: ' + data)  # show in terminal
            #racer = input("Enter 1 of 2 om voor p1 of p2 een sensor signaal te simuleren...")
    
    client_socket.close()  # close the connection


if __name__ == '__main__':
    # Zet de pinmode op Broadcom SOC.
    GPIO.setmode(GPIO.BCM)
    # Zet waarschuwingen uit.
    GPIO.setwarnings(False)
    # Zet de GPIO pin als ingang.
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Gebruik een interrupt, wanneer actief run subroutinne 'gedrukt'
    GPIO.add_event_detect(2, GPIO.RISING, callback=singal_found_p1, bouncetime=200)
    GPIO.add_event_detect(3, GPIO.RISING, callback=singal_found_p2, bouncetime=200)
    client_program()
