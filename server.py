import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        threading.Thread.__init__(self)
        self.clientSocket =  clientSocket
        self.clientAddress = clientAddress
        print("New connection added from ", clientAddress)

    def run(self):
        msg = "welcome".encode()
        self.clientSocket.send(msg)
        while True:
            data = self.clientSocket.recv(1024).decode()
            if data == "bye":
                break
            msg = str(eval(data)).encode()
            self.clientSocket.send(msg)
        self.clientSocket.close()

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started!")
print("Waiting for connection requests")

while True:
    server.listen()
    clientSocket, clientAddress = server.accept()
    newThread = ClientThread(clientSocket, clientAddress)
    newThread.start()