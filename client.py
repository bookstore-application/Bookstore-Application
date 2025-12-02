import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    in_data = client.recv(1024).decode()
    print("Message from the server ", in_data)
    out_data = input("Enter your question: ")
    client.send(out_data.encode())
    if out_data == "bye":
        break
client.close()