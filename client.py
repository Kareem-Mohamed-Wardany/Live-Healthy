# imports
import socket
import sys
import threading


# client class
class Client:
    # format for messages
    FORMAT = "utf-8"
    HOST = "127.0.0.1"
    PORT = 4073

    # creating a socket for client
    # initializing
    # name of a client, chanel , client adress
    def __init__(self, name, addr, chnl):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.channel = chnl
        self.clientsocket.connect(addr)

    # function for sending messages to a server
    def writeToServer(self, userInput=None):
        # name input
        if userInput is not None:
            message = f"{self.name}: {userInput}"

            # send name to server
            self.clientsocket.send(message.encode(self.FORMAT))

    def receiveFromServer(self, q):
        while True:
            try:
                # recieve a message from server
                message = self.clientsocket.recv(1024).decode(self.FORMAT)

                # if the message contains a keyword "+getName+Channel", send name and channel to server
                if message == "getData":
                    self.clientsocket.send(
                        f"{self.name}&,&{self.channel}".encode(self.FORMAT)
                    )
                elif message != "Please enter message" or message != "":
                    q.put(message)
            except Exception:
                self.clientsocket.close()
                break

    def end(self):
        self.clientsocket.close()


# def StartClient(name, Channel):
#     # taking inputs from the user on launch
#     # write an error if input is incorrect
#     # INPUT: NAME, CHANELNAME
#     # creating a client
#     ADDR = ("127.0.0.1", 4073)
#     client = Client(name, ADDR, Channel)

#     # creating threads for writing and listenting
#     # recieve thread
#     receiveThread = threading.Thread(target=client.receiveFromServer)
#     receiveThread.start()

#     # write thread
#     writeThread = threading.Thread(target=client.writeToServer)
#     writeThread.start()
