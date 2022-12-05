import socket
import errno
import time
import threading
import queue


class Client:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()

        self.running = True
        self.writing = True
        self.reading = True
        self.processing = True

        self.conn = None

        # Create threads
        self.readThread = threading.Thread(target=self.read)
        self.writeThread = threading.Thread(target=self.write)
        self.uiThread = threading.Thread(target=self.ui)

    def write(self):
        print("Write thread started")
        while self.writing:
            if not self.running and self.oBuffer.empty():
                self.writing = False
            if not self.oBuffer.empty():
                self.conn.sendall(self.oBuffer.get().encode("utf-8"))
                time.sleep(0.1)

    def read(self):
        print("Read thread started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            self.conn.connect((self.HOST, self.PORT))
            self.conn.setblocking(False)

            while self.reading:
                # Program has stopped running - self terminate and close the socket.
                if not self.running:
                    self.reading = False
                    break

                # attempt to read data from the socket:
                try:
                    data = self.conn.recv(1024)
                    if data:
                        message = data.decode("utf-8")
                        self.iBuffer.put(message)

                # Handle errors that come from the socket
                except socket.error as e:
                    err = e.args[0]
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        time.sleep(0.1)
                    else:
                        self.running = False
                        self.conn.shutdown(socket.SHUT_RDWR)


    def ui(self):
        # Handle incoming messages from the server - i.e. at the moment, show them to the user
        while self.running:
            if not self.iBuffer.empty():
                message = self.iBuffer.get()
                print(message)

    def process(self):
        # start the different threads for reading, writing and ui
        self.readThread.start()
        self.writeThread.start()
        self.uiThread.start()

        # handle shutting the client app down
        while self.processing:
            if not self.running:
                self.processing = False
                break

            message = input("Please enter a command: ")
            self.oBuffer.put(message)

            if message == "Quit":
                self.running = False

        self.readThread.join()
        self.writeThread.join()
        self.uiThread.join()


if __name__ == "__main__":
    client = Client("127.0.0.1", 50001)
    client.process()
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
