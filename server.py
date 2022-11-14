import socket
import gamefunctions
from enum import Enum

class State(Enum):
    Start = 1
    Login = 2
    Menus = 3
    Play = 4
    Error = 99

# def readFile(name):
#     dataLine = name.readLine()
#     decryptedLine = decrypt(dataLine)


class Server:
    def __init__(self, host, port):
        # define network parameters
        self.HOST = host
        self.PORT = port
        self.currentState = State.Start
        self.previousState = None
        self.running = True
        self.counter = 0

    def run(self):
        play = True
        # define socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # set the socket to re-useable
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to address and port
            s.bind((self.HOST, self.PORT))
            # listen on the socket for a connection
            s.listen()

            # accept a client connection define the client socket and address
            client_connection, address = s.accept()
            print(f"connection established with {address}.")
            client_connection.send(bytes("Welcome to the Game Server\n**************************\n\nPlease type Login and press enter to log in to the server", "utf-8"))

            while play:
                data = client_connection.recv(1024)
                if not data:
                    break
                # Do some processing
                message = data.decode().upper()
                # Handle termination
                if message == "Quit":
                    message = "Acknowledge quitting"
                    self.running = False
                else:
                    # State machines cover the following:
                    #
                    if self.currentState == State.Start:
                        if message.startswith("LOGIN"):
                            self.previousState = self.currentState
                            self.currentState = State.Login
                            message = "Login Menu Loading..."
                        # elif message.startswith("Login"):
                        #     self.previousState = self.currentState
                        #     self.currentState = State.Login
                        #     message = "Moving to Login"
                        else:
                            message = "You must type in Login and press enter"
                    elif self.currentState == State.Login:
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
                        if message.startswith("ADMIN"):
                            if message.endswith("PASSWORD"):
                                self.previousState = self.currentState
                                self.currentState = State.Menus
                                message = "Moving to Menus..."
                        else:
                            message = "Echoing: " + message
                    elif self.currentState == State.Menus:
                        if message.startswith("Echo"):
                            self.previousState = self.currentState
                            self.currentState = State.Echo
                            message = "Moving to Echo"
                        else:
                            try:
                                cmd, arg = message.split(" ", 1)
                            except ValueError:
                                cmd = "Error"

                            try:
                                value = int(arg)
                            except ValueError:
                                value = 0
                            message = str(self.counter)

                    else:
                        message = "An Error has occurred, returning to start state"
                        self.currentState = State.Start
                        self.previousState = State.Error

                # send back the response
                client_connection.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    server = Server("127.0.0.1", 50001)
    server.run()

