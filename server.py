import socket
import gamefunctions
from enum import Enum

class State(Enum):
    Start = 1
    Login = 2
    Menus = 3
    Play = 4
    Error = 99



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
            client_connection.send(bytes("Welcome to the Game Server\n**************************\n\nOptions:\nPress 1 to Enter your name.\nPress 2 to roll a dice", "utf-8"))

            while play:
                    data = client_connection.recv(1024)
                    if not data:
                        break
                    # Do some processing
                    message = data.decode().upper()
                    if message.startswith("2"):
                        message = str(gamefunctions.d6())
                        client_connection.send(message.encode())
                    # elif message.startswith("1"):
                    #     # Return a message to the client
                    #     message = "Please type in your name and press enter\n"
                    #     client_connection.send(message.encode())
                    #     client_name = data.decode().upper


if __name__ == "__main__":
    server = Server("127.0.0.1", 50001)
    server.run()

