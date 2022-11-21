import socket

class Client:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))

            while True:
                message = input("Please enter a command: ")
                s.sendall(message.encode("UTF-8"))

                data = s.recv(1024)
                print(f"Received {data!r}")

                response = data.decode("utf-8")

                if response.startswith("COMPLEXTEST"):
                    print("Entering a different style of state")
                    while True:
                        message = input("Please enter a message: ")
                        s.sendall(message.encode())

                        if message == "TERMINATE":
                            data = s.recv(1024)
                            print(f"Received {data!r}")
                            break
                if message == "Quit":
                    s.shutdown(socket.SHUT_RDWR)
                    break

if __name__ == "__main__":
    client = Client("127.0.0.1", 50001)
    client.run()
# # create our connection socket, IPv4 and streaming connection
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# play = True
# user_doing_stuff = True
#
# # connect to the server
# s.connect(("127.0.0.1", 50001))
#
# while play:
#     # set the buffer size to 1024 and decode to UTF-8 and print the message
#     message_received = s.recv(1024)
#     print(message_received.decode("utf-8"))
#     message_send = input("Type option and press enter: ").upper()
#     if message_send == "QUIT":
#         play = False
#         # shutdown socket connection to server
#         s.shutdown(socket.SHUT_RDWR)
#         break
#     else:
#         s.sendall(message_send.encode())
#
#
