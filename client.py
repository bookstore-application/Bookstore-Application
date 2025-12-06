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
            print("Login successful!!!")
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
    def __init__(self, manager, username):
        Frame.__init__(self)
        self.manager = manager
        self.username = username
        self.bookList = []
        self.master.title("Inventory Management")
        self.master.resizable(True, True)

        self.pack(padx=10, pady=10)


        addBookFrame = LabelFrame(self, text="Add Book", padx=10, pady=10)
        addBookFrame.pack(padx=5, pady=5, fill=BOTH)


        frame1 = Frame(addBookFrame)
        frame1.pack(padx=5, pady=5, fill=X)
        Label(frame1, text="Book Id:", width=15, anchor=W).pack(side=LEFT)
        self.bookIDEntry = Entry(frame1, width=30)
        self.bookIDEntry.pack(side=LEFT, fill=X, expand=True)

        frame2 = Frame(addBookFrame)
        frame2.pack(padx=5, pady=5, fill=X)
        Label(frame2, text="Title:", width=15, anchor=W).pack(side=LEFT)
        self.titleEntry = Entry(frame2, width=30)
        self.titleEntry.pack(side=LEFT, fill=X, expand=True)

        frame3 = Frame(addBookFrame)
        frame3.pack(padx=5, pady=5, fill=X)
        Label(frame3, text="Authors:", width=15, anchor=W).pack(side=LEFT)
        self.authorsEntry = Entry(frame3, width=30)
        self.authorsEntry.pack(side=LEFT, fill=X, expand=True)

        frame4 = Frame(addBookFrame)
        frame4.pack(padx=5, pady=5, fill=X)
        Label(frame4, text="Genre:", width=15, anchor=W).pack(side=LEFT)
        self.genreEntry = Entry(frame4, width=30)
        self.genreEntry.pack(side=LEFT, fill=X, expand=True)

        frame5 = Frame(addBookFrame)
        frame5.pack(padx=5, pady=5, fill=X)
        Label(frame5, text="Quantity:", width=15, anchor=W).pack(side=LEFT)
        self.quantityEntry = Entry(frame5, width=30)
        self.quantityEntry.pack(side=LEFT, fill=X, expand=True)

        frame6 = Frame(addBookFrame)
        frame6.pack(padx=5, pady=5, fill=X)
        Label(frame6, text="Price:", width=15, anchor=W).pack(side=LEFT)
        self.priceEntry = Entry(frame6, width=30)
        self.priceEntry.pack(side=LEFT, fill=X, expand=True)

        addButtonFrame = Frame(addBookFrame)
        addButtonFrame.pack(padx=5, pady=5)
        self.addButton = Button(addButtonFrame, text="Add", width=10, command=self.addBook)
        self.addButton.pack(side=RIGHT)

        updateFrame = LabelFrame(self, text="Update Inventory", padx=10, pady=10)
        updateFrame.pack(padx=5, pady=5, fill=BOTH)

        frame7 = Frame(updateFrame)
        frame7.pack(padx=5, pady=5, fill=X)
        Label(frame7, text="Book Id:", width=20, anchor=W).pack(side=LEFT)
        self.updateBookIDEntry = Entry(frame7, width=25)
        self.updateBookIDEntry.pack(side=LEFT, fill=X, expand=True)

        frame8 = Frame(updateFrame)
        frame8.pack(padx=5, pady=5, fill=X)
        Label(frame8, text="# of books to be added:", width=20, anchor=W).pack(side=LEFT)
        self.updateQuantityEntry = Entry(frame8, width=25)
        self.updateQuantityEntry.pack(side=LEFT, fill=X, expand=True)


        updateButtonFrame = Frame(updateFrame)
        updateButtonFrame.pack(padx=5, pady=5)
        self.updateButton = Button(updateButtonFrame, text="Update", width=10, command=self.updateInventory)
        self.updateButton.pack(side=RIGHT)

        statsFrame = LabelFrame(self, text="Statistics", padx=10, pady=10)
        statsFrame.pack(padx=5, pady=5, fill=BOTH)

        self.statsVar = IntVar()
        self.statsVar.set(1)

        Radiobutton(statsFrame, text="Top-Selling Author", variable=self.statsVar,
                    value=1).pack(anchor=W, padx=5, pady=2)
        Radiobutton(statsFrame, text="Most Profitable Genre", variable=self.statsVar,
                    value=2).pack(anchor=W, padx=5, pady=2)
        Radiobutton(statsFrame, text="Busiest Cashier", variable=self.statsVar,
                    value=3).pack(anchor=W, padx=5, pady=2)

        generateButtonFrame = Frame(statsFrame)
        generateButtonFrame.pack(padx=5, pady=5)
        self.generateButton = Button(generateButtonFrame, text="Generate", width=10,
                                     command=self.generateStatistics)
        self.generateButton.pack(side=RIGHT)

        closeButtonFrame = Frame(self)
        closeButtonFrame.pack(padx=5, pady=10)
        self.closeButton = Button(closeButtonFrame, text="Close", width=10,
                                  command=self.closePanel)
        self.closeButton.pack()
    def addBook(self):
        add_book_data = f"addbook;{self.bookIDEntry.get()};{self.titleEntry.get()};{self.authorsEntry.get()};{self.genreEntry.get()};{self.priceEntry.get()};{self.quantityEntry.get()}"
        self.manager.send(add_book_data.encode())
        response = self.manager.recv(1024).decode().split(";")

        if response[0] == "addbookconfirmation":
            messagebox.showinfo("addbook confirmed", "Added new book")
            self.bookIDEntry.delete(0, END)
            self.titleEntry.delete(0, END)
            self.authorsEntry.delete(0, END)
            self.genreEntry.delete(0, END)
            self.quantityEntry.delete(0, END)
            self.priceEntry.delete(0, END)

        else:
            messagebox.showerror("addbook failured", response[1])


    def updateInventory(self):
        update_data = f"updatequantity;{self.updateBookIDEntry.get()};{self.updateQuantityEntry.get()}"
        self.manager.send(update_data.encode())
        response = self.manager.recv(1024).decode().split(";")

        if response[0]=="updatequantityconfirmation":
            messagebox.showinfo("updatequantity confirmed", "Updated quantity")
        else:
            messagebox.showerror("updatequantity failured", response[1])

    def generateStatistics(self):
        choice = self.statsVar.get()

        # labels = {1:"report1", 2:"report2", 3:"report3"}
        # request = f"{labels[choice]}"
        request = f"report{choice}"

        self.manager.send(request.encode())
        response = self.manager.recv(1024).decode().split(";")

        if response[0]=="report2":
            messagebox.showinfo(f"report{choice}",f"{response[1]}: {response[2]}")
        else:
            messagebox.showerror("Error", response[1])

    def closePanel(self):
        try:
            self.manager.send("closeconnection".encode())
            self.manager.close()
        except Exception as e:
            print(f"Error: {e}")

        print("Closing Panel")
        self.master.destroy()


in_data = client.recv(1024).decode()
print("Message from the server:", in_data)

window = LoginScreen(client)
window.mainloop()

client.close()