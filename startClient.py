import socket
import time

def current_milli_time():
    return str(round(time.time() * 1000))

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    clientName = "StartClient"
    message = clientName

    while True:
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        #print('Received from server: ' + data)  # show in terminal
        racer = input("Enter 1 of 2 om voor p1 of p2 een sensor signaal te simuleren...")
        message = "p" + racer + clientName + ":" + current_milli_time()  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
