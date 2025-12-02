from socket import *
from threading import *


class ClientThread(Thread):
    def __init__(self, clientSocket, clientAddress, user_records):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.user_records = user_records
        print("New connection added from", clientAddress)

    def run(self):
        msg = "connectionsuccess".encode()
        self.clientSocket.send(msg)

        try:
            data = self.clientSocket.recv(1024).decode()
            data = data.split(";")

            username = data[1]
            password = data[2]

            if username == "" or password == "":
                msg = f"loginfailure".encode()
                self.clientSocket.send(msg)
                self.clientSocket.close()
                return


            found = False
            user_role = ""
            for record in self.user_records:
                record = record.strip()

                record = record.split(";")
                stored_username = record[0]
                stored_password = record[1]

                if username == stored_username and password == stored_password:
                    found = True
                    user_role = record[2]
                    break

            if found:
                msg = f"loginsuccess;{username};{user_role}".encode()
            else:
                msg = f"loginfailure".encode()

            self.clientSocket.send(msg)


        except Exception:
            print(f"Error handling client {self.clientAddress}")
        finally:
            self.clientSocket.close()
            print(f"Connection closed from {self.clientAddress}")


HOST = "127.0.0.1"
PORT = 5000

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started!")
print("Waiting for connection requests")

try:
    file =  open("users.txt", "r")
    user_records = file.readlines()
    file.close()
except FileNotFoundError:
    print("users.txt file not found")
    exit(1)

while True:
    server.listen()
    clientSocket, clientAddress = server.accept()

    newThread = ClientThread(clientSocket, clientAddress, user_records[:]) #passes a copy to each thread..
    newThread.start()
