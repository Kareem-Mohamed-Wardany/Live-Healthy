#imports
import sys
import socket
import threading

class Server:

    #format for messages
    FORMAT = "utf-8"
    HOST = "127.0.0.1"
    PORT = 4073

    #creating a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #server init function
    def __init__(self,addr):
        self.server.bind(addr)
        self.server.listen()
        #making rooms a dictionary type for all rooms and their clients
        self.rooms = {}
        self.listOfClients = []
        self.nicknames = []

    #send a message to all clients
    def sendToAll(self,client,message,roomName):
        if roomName in self.rooms:
            for eachClient in self.rooms[roomName]:
                    eachClient.send(message)

    #remove a client from a room
    def removeClient(self,client):
        for room in self.rooms:
            if client in self.rooms[room]:
                self.rooms[room].remove(client)
                break


    #create a new room and join it
    def createRoom(self, roomName, nickname, client):
        #removing a client from the old room so he can join the new one
        self.removeClient(client)
        #creating and joining the new room
        self.rooms[roomName] = [client]
        print(f"{nickname} created and joined room {roomName}")

    #function that handles client interaction (sending messages)
    def clientInteraction(self,client,roomName):
        while True:
            try:
                message = client.recv(1024)

                self.sendToAll(client, message, roomName)
            except:
                #deleting client as he is no longer able to send messages
                index = self.listOfClients.index(client)
                self.listOfClients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                #removing nickname from the list
                print(f"{self.nicknames[index]} has left the server")

                self.removeClient(client)
                self.nicknames.remove(nickname)
                break

    def RunServer(self):
        while True:
            #adding a client to a server
            client, addr = self.server.accept()
            print(f"Connection occured from {str(addr)}")
            #getting data from the client to add to the list of clients
            client.send("getData".encode(self.FORMAT))
            try:
                response = client.recv(1024).decode(self.FORMAT)
                splitRepsonse = response.split("&,&")
                nickname = splitRepsonse[0]
                roomName = splitRepsonse[1]
                #check if room exists
                if (roomName in self.rooms):
                    self.rooms[roomName].append(client)
                else:
                    #if no, create it and join
                    self.createRoom(roomName, nickname, client)
                    print(f"user {nickname} created and joined room {roomName}")

                print(f"New clients nickname is {nickname}")

                #adding his info to the list
                self.nicknames.append(nickname)
                self.listOfClients.append(client)

                #threads for each client
                thread = threading.Thread(target=self.clientInteraction,args=(client,roomName,))
                thread.start()
            except:
                pass


def main():
    ADDRESS = ('127.0.0.1',4073)
    s = Server(ADDRESS)
    print("Server started")
    s.RunServer()


if __name__ == "__main__":
    main()