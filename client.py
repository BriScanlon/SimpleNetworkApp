import socket
# create our connection socket, IPv4 and streaming connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
play = True
user_doing_stuff = True

# connect to the server
s.connect(("127.0.0.1", 50001))

while play:
    # set the buffer size to 1024 and decode to UTF-8 and print the message
    message_received = s.recv(1024)
    print(message_received.decode("utf-8"))
    message_send = input("Type option and press enter: ").upper()
    if message_send == "QUIT":
        play = False
        # shutdown socket connection to server
        s.shutdown(socket.SHUT_RDWR)
        break
    else:
        s.sendall(message_send.encode())


