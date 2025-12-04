from socket import *
from tkinter import *
from tkinter import messagebox
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

client = socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))


class LoginScreen(Frame):
    def __init__(self, client):
        Frame.__init__(self)
        self.pack()
        self.client = client
        self.master.title("Login")

        self.frame1 = Frame(self)
        self.frame1.pack(padx = 5, pady=5)

        self.userNameLabel = Label(self.frame1, text="Username: ")
        self.userNameLabel.pack(padx=5, pady=5, side=LEFT)

        self.userNameEntry = Entry(self.frame1)
        self.userNameEntry.pack(padx=5, pady=5, side=LEFT)

        self.frame2 = Frame(self)
        self.frame2.pack(padx= 5, pady=5)

        self.passwordLabel = Label(self.frame2, text="Password: ")
        self.passwordLabel.pack(padx=5, pady=5, side=LEFT)

        self.passwordEntry = Entry(self.frame2, show="*")
        self.passwordEntry.pack(padx=5, pady=5, side=LEFT)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady= 5)

        self.loginButton = Button(self.frame3, text="Login", command = self.ButtonPressed)
        self.loginButton.pack(padx=5, pady=5, side=LEFT)

    def ButtonPressed(self):
        out_data = f"login;{self.userNameEntry.get()};{self.passwordEntry.get()}"
        self.client.send(out_data.encode())

        response = self.client.recv(1024).decode().split(";")

        if response[0] == "loginsuccess":
            print("Login successfulllll")
            username = response[1]
            role = response[2]

            self.master.destroy()

            if role == "Cashier":
                CashierPanel(self.client, username)
            elif role == "Manager":
                ManagerPanel(self.client, username)
            else:
                print("Invalid role")
        elif response[0] == "loginfailure":
            messagebox.showerror("Login Failed", "Invalid username or password!")



class CashierPanel(Frame):
    def __init__(self, cashier, username):
        Frame.__init__(self)
        self.cashier = cashier
        self.username = username
        self.bookList = [] # keep track of added books
        self.pack()
        self.master.title("Transaction")

        self.frame1 = Frame(self)
        self.frame1.pack(padx = 5, pady=5)

        self.bookIDLabel = Label(self.frame1, text="Book ID: ")
        self.bookIDLabel.pack(padx=5, pady=5, side=LEFT)

        self.bookIDEntry = Entry(self.frame1)
        self.bookIDEntry.pack(padx=5, pady=5, side=LEFT)

        self.frame2 = Frame(self)
        self.frame2.pack(padx= 5, pady=5)

        self.quantityLabel = Label(self.frame2, text="Quantity: ")
        self.quantityLabel.pack(padx=5, pady=5, side=LEFT)

        self.quantityEntry = Entry(self.frame2)
        self.quantityEntry.pack(padx=5, pady=5, side=LEFT)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady= 5)

        self.addButton = Button(self.frame3, text="Add Book", command = self.addButtonPressed)
        self.addButton.pack(padx=5, pady=5, side=LEFT)

        self.frame3 = Frame(self) #  add book
        self.frame3.pack(padx = 5, pady = 5)

        self.addLabel = Label(self.frame3, text="Books Added:")
        self.addLabel.pack(padx = 5, pady = 5, side = LEFT)

        self.frame4 = Frame(self)
        self.frame4.pack(padx = 5, pady = 5)

        self.bookEntry = Text(self.frame4, width = 25, height = 5)
        self.bookEntry.pack(padx = 5, pady = 5, side = LEFT)

        self.frame5 = Frame(self) # discount entry
        self.frame5.pack(padx = 5, pady = 5)

        self.discountLabel = Label(self.frame5, text="Discount Code: ")
        self.discountLabel.pack(padx = 5, pady = 5, side = LEFT)

        self.discountEntry = Entry(self.frame5)
        self.discountEntry.pack(padx = 5, pady= 5, side = LEFT)

        self.frame6 = Frame(self) # close button
        self.frame6.pack(padx = 5, pady = 5)

        self.closeButton = Button(self.frame6, text = "Close", command = self.closeButtonPressed)
        self.closeButton.pack (padx = 5, pady = 5, side =LEFT)

        self.transactionButton = Button(self.frame6, text="Complete Transaction", command = self.transactionButtonPressed)
        self.transactionButton.pack(padx = 5, pady = 5, side = LEFT)


    def closeButtonPressed(self):
        print("close button pressed")

    def addButtonPressed(self):
        print("add Button pressed")
        book_id = self.bookIDEntry.get()
        quantity = self.quantityEntry.get()
        book = f"{book_id}-{quantity}"
        self.bookList.append(book)
        self.bookEntry.insert(END, book + "\n")

    def transactionButtonPressed(self):
        print("Transaction button pressed")
        date = datetime.now()
        discount_code = self.discountEntry.get()
        books = ";".join(self.bookList)
        data_out = f"transaction;{date};{discount_code};{books}"

        self.cashier.send(data_out.encode())

        #if response[0] == "transactionconfirmation": h
        #elif response[0] == "transactionfailure":




class ManagerPanel(Frame):
    def __init__(self, client, username):
        Frame.__init__(self)
        self.client = client
        self.username = username


in_data = client.recv(1024).decode()
print("Message from the server:", in_data)

window = LoginScreen(client)
window.mainloop()

client.close()