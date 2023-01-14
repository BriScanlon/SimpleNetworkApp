import errno
import threading
import time
from socket import socket

from AbstractedServer import Server
from enum import Enum


class State(Enum):
    Start = 1
    Login = 2
    Menus = 3
    Play = 4
    Complex = 5
    Error = 99


# def readFile(name):
#     dataLine = name.readLine()
#     decryptedLine = decrypt(dataLine)


class abstractServer:

    def __init__(self, host="127.0.0.1", port=50000):
        self.server = Server(host, port)

        # Variables dealing with state management and functionality
        self.currentState = State.Start
        self.previousState = None
        self.counter = 0
        self.messages = []

        # message handling variables
        self.running = True

        # create threads
        self.readThread = threading.Thread(target=self.read)
        self.writeThread = threading.Thread(target=self.write)

    def write(self):
        print("Write Thread started")
        while self.writing:
            if not self.running and self.oBuffer.empty():
                self.writing = False
            if not self.oBuffer.empty():
                self.client_connection.sendall(self.oBuffer.get().encode("utf-8"))
                time.sleep(1)

    def read(self):
        print("Read thread started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_object:

            # set the socket to re-useable
            socket_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to address and port
            socket_object.bind((self.HOST, self.PORT))
            # listen on the socket for a connection
            socket_object.listen()
            self.client_connection, self.addr = socket_object.accept()

            with self.client_connection:
                self.client_connection.setblocking(False)
                # accept a client connection define the client socket and address
                print(f"connection established with {self.addr}.")
                while self.reading:
                    if not self.reading:
                        self.reading = False
                        break
                # attempt to read data from the data socket
                    try:
                        data = self.client_connection.recv(1024)
                        if data:
                            message = data.decode("utf-8")
                            self.iBuffer.put(message)
                    except socket.error as error:
                        err = error.args[0]
                        # no data on socket, but socket still exists - wait and retry
                        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                            time.sleep (1)
                            print(f"no data to read from {self.addr}")
                        else:
                            # an actual error has occurred, shut down the program as our sole client has now disconnected
                            self.running = False
                            self.client_connection.shutdown(socket.SHUT_RDWR)
                # self.client_connection.send(
                #     bytes("Welcome to the Game Server.  Please type Login and press enter to log in to the server",
                #           "utf-8"))

    def process(self):
        # start the reading and writing threads
        self.server.process()

        # how to handle the program shutting down
        while self.running:
            # only try to process a message if there is a message in the incoming message buffer
            message = self.server.getMessage()
            if message:
                if message == "Quit":
                    message = "Acknowledge quitting, good-bye"
                    self.running = False

                else:
                    if self.currentState == State.Start:
                        message = self.start(message)
                    elif self.currentState == State.Login:
                        message = self.login(message)
                    elif self.currentState == State.Menus:
                        message = self.menus(message)
                    elif self.currentState == State.Play:
                        message = self.play(message)
                    elif self.currentState == State.Complex:
                        message = self.complex(message)
                    else:
                        message = self.handle_error(message)
                if message:
                    self.server.pushMessage(message)
        self.server.quit()


    def start(self, message):
        if message.startswith("LOGIN"):
            self.previousState = self.currentState
            self.currentState = State.Login
            message = "Login Menu Loading..."
        else:
            message = "You must type in Login and press enter"
        return message

    def complex(self, message):
        self.messages.append(message)
        while True:
            # intereact with the buffer
            if not self.iBuffer.empty():
                message = self.iBuffer.get()
                print(message)
                # handle termination
                if message == "TERMINATE":
                    message = "".join(self.messages)
                    break
                else:
                    self.messages.append(message)

        self.currentState = State.Start
        self.previousState = State.Complex
        return message

    def login(self, message):
        # while unameReceived is false, skip asking for the password and ask for the username instead
        # when unameReceived is true, ask for the password.
        if self.unameReceived:
            if message.endswith("PASSWORD"):
                self.previousState = self.currentState
                self.currentState = State.Menus
                message = "Moving to Menus..."
            else:
                self.unameReceived = False
                message = "Incorrect password..."
        else:
            if message.startswith("ADMIN"):
                self.unameReceived = True
                message = "Password?"
        print(message)
        return message

    def menus(self, message):
        if message.startswith("Menus"):
            self.previousState = self.currentState
            self.currentState = State.Menus
            message = "Moving to Menus"
        return message

    def play(self, message):
        if message.startswith("Play"):
            self.previousState = self.currentState
            self.currentState = State.Play
            message = "Moving to Play"
        return message

    def complex(self, message):
        # Complex now only needs to manage the state itself, as the network flow change is handled by the network and
        # the buffers.
        if message == "TERMINATE":
            message = "".join(self.messages)
            self.currentState = State.Start
            self.previousState = State.Complex
        else:
            self.messages.append(message)
            message = None
        return message


    def handle_error(self, message):
        message = "An Error has occurred, returning to start state"
        self.currentState = State.Start
        self.previousState = State.Error
        return message


if __name__=="__main__":
    server = Server("127.0.0.1", 50001)
    server.process()
