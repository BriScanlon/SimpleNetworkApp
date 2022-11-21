import socket
import gamefunctions
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


class Server:

    def __init__(self, host="127.0.0.1", port=50000):
        # define network parameters
        self.HOST = host
        self.PORT = port
        self.currentState = State.Start
        self.previousState = None
        self.running = True
        self.counter = 0
        self.messages = []

        self.client_connection = None
        self.addr = None

    def start(self, message):
        if message.startswith("LOGIN"):
            self.previousState = self.currentState
            self.currentState = State.Login
            message = "Login Menu Loading..."
        else:
            message = "You must type in Login and press enter"
        return message

    def complex(self, message):
        while True:
            data = self.client_connection.recv(1024)
            if not data:
                self.running = False
                message = "Error"
                break

            message = data.decode("utf-8")
            print(message)
            # Handle termination
            if message == "TERMINATE":
                message = "".join(self.messages)
                break
            else:
                self.messages.append(message)

        self.currentState = State.Start
        self.previousState = State.Complex
        return message

    def login(self, message, unameReceived=None):
        # while unameReceived is false, skip asking for the password and ask for the username instead
        # when unameReceived is true, ask for the password.
        if unameReceived:
            if message.endswith("PASSWORD"):
                self.previousState = self.currentState
                self.currentState = State.Menus
                message = "Moving to Menus..."
            else:
                unameReceived = False
                message = "Incorrect password..."
        else:
            if message.startswith("ADMIN"):
                unameReceived = True
                message = "Password?"
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

    def handleError(self, message):
        message = "An Error has occurred, returning to start state"
        self.currentState = State.Start
        self.previousState = State.Error
        return message

    def run(self):
        # play = True
        # define socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # set the socket to re-useable
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to address and port
            s.bind((self.HOST, self.PORT))
            # listen on the socket for a connection
            s.listen()
            self.client_connection, self.addr = s.accept()

            with self.client_connection:
                # accept a client connection define the client socket and address
                print(f"connection established with {self.addr}.")
                self.client_connection.send(bytes("Welcome to the Game Server.  Please type Login and press enter to log in to the server", "utf-8"))

                while self.running:
                    if self.currentState == State.Complex:
                        message = self.complex(message)
                    else:
                        data = self.client_connection.recv(1024)
                        if not data:
                            break
                        message = data.decode("utf-8")

                        if message == "Quit":
                            message = "Acknowledge quitting"
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
                            else:
                                message = self.handleError(message)
                self.client_connection.sendall(message.encode("utf-8"))


if __name__ == "__main__":
    server = Server("127.0.0.1", 50001)
    server.run()
