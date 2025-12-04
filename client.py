from socket import *
from tkinter import *
from tkinter import messagebox

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
        Frame.__init__(self)
        self.username = username
        self.pack()
        self.master.title("Transaction")

        self.frame1 = Frame(self)
        self.frame1.pack(padx = 5, pady=5)



        self.frame2 = Frame(self)
        self.frame2.pack(padx= 5, pady=5)



        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady= 5)



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