from socket import *
from threading import *


class ClientThread(Thread):
    def __init__(self, clientSocket, clientAddress, user_records, discount_records):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.user_records = user_records
        self.discount_records = discount_records
        print("New connection added from", clientAddress)

    def run(self):
        msg = "connectionsuccess".encode()
        self.clientSocket.send(msg)

        try:
            while True:
                data = self.clientSocket.recv(1024).decode()
                if not data:
                    break

                data = data.split(";")

                if data[0] == "login":
                    username = data[1]
                    password = data[2]

                    if username == "" or password == "":
                        msg = f"loginfailure".encode()
                        self.clientSocket.send(msg)
                        continue

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

                elif data[0] == "transaction":
                    date = data[1]
                    discount_code = data[2]
                    books = data[3]

                    if books == "":
                        msg = f"transactionfailure;bookNotAdded".encode()
                        self.clientSocket.send(msg)
                        continue

                    found = False
                    for record in self.discount_records:
                        record = record.strip()
                        if record == discount_code:
                            found = True
                            break

                    if not found:
                        msg = f"transactionfailure;incorrectDiscountCode".encode()
                    else:
                        msg = f"transactionconfirmation".encode()

                    self.clientSocket.send(msg)

                elif data[0] == "addbook":
                    if not all(data[1:7]):
                        msg = f"addbookfailure;Fill in all the fields".encode()
                        self.clientSocket.send(msg)
                        continue

                    bookid = data[1].strip()
                    title = data[2].strip()
                    author = data[3].strip()
                    genre = data[4].strip()
                    quantity = data[5].strip()
                    price = data[6].strip()

                    try:
                        quantity_int = float(quantity)
                        price_float = float(price)

                        if quantity_int < 0  or price_float <0:
                            msg = f"addbookfailure;Price and quantity should be positive".encode()
                            self.clientSocket.send(msg)
                            continue
                        with open("inventory.txt", "a") as inventory_file:
                            inventory_file.write(f"{bookid};{title};{author};{genre};{price};{quantity}\n")

                        msg = f"addbookconfirmation".encode()
                        self.clientSocket.send(msg)
                    except Exception as e:
                        print(f"Error writing to inventory: {e}")
                        msg = f"addbookfailure;Exception".encode()
                        self.clientSocket.send(msg)

                elif data[0] == "updatequantity":
                    if not data[1] or not data[2]:
                        msg = f"updatequantityfailure".encode()
                        self.clientSocket.send(msg)
                        continue

                    bookid = data[1].strip()
                    added_quantity = int(data[2].strip())

                    try:
                        with open("inventory.txt", "r") as f:
                            lines = f.readlines()

                        updated = False
                        counter = 0
                        for line in lines:
                            parts = line.strip().split(";")
                            if parts[0] == bookid:
                                current_quantity = int(parts[5])
                                new_quantity = current_quantity + added_quantity
                                parts[5] = str(new_quantity)
                                lines[counter] = ";".join(parts) + "\n"
                                updated = True
                                break
                            counter += 1

                        if updated:
                            with open("inventory.txt", "w") as f:
                                f.writelines(lines)
                            msg = f"updatequantityconfirmation".encode()
                        else:
                            msg = f"updatequantityfailure;booknotfound".encode()

                        self.clientSocket.send(msg)
                    except Exception as e:
                        print(f"Error updating inventory: {e}")
                        msg = (f"updatequantityfailure;{e}").encode()
                        self.clientSocket.send(msg)
                elif data[0] == "report2":
                    if data[1] == "Top-selling author":
                        try:
                            topselling, authorsales = self.get_topselling_auther()
                            msg = f"report2;{topselling};{authorsales[topselling]}".encode()
                            self.clientSocket.send(msg)
                        except Exception as e:
                            msg = f"report2;{e}".encode()
                            self.clientSocket.send(msg)
        except Exception as e:
            print(f"Error handling client {self.clientAddress}: {e}")
        finally:
            self.clientSocket.close()
            print(f"Connection closed from {self.clientAddress}")

    def get_topselling_auther(self):
        author_sales = {}

        with open("inventory.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            inventory_data = line.strip().split(";")
            sale = int(inventory_data[5])

            authors = inventory_data[2]

            for author in authors.split("and"):
                author = author.strip()
                author_sales[author] = author_sales.get(author, 0) + int(sale)
        top_selling = max(author_sales, key=lambda author: author_sales[author])
        return top_selling, author_sales



HOST = "127.0.0.1"
PORT = 5000

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started!")
print("Waiting for connection requests")

try:
    user_file = open("users.txt", "r")
    user_records = user_file.readlines()
    user_file.close()
except FileNotFoundError:
    print("users.txt file not found")
    exit(1)

try:
    discountFile = open("discountcodes.txt", "r")
    discount_records = discountFile.readlines()
    discountFile.close()
except FileNotFoundError:
    print("discountcodes.txt file not found")
    exit(1)

try:
    with open("inventory.txt", "a"):
        pass
except Exception:
    print("inventory.txt cannot be created")
    exit(1)

while True:
    server.listen()
    clientSocket, clientAddress = server.accept()
    newThread = ClientThread(clientSocket, clientAddress, user_records[:], discount_records[:])
    newThread.start()