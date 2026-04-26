from tkinter import *
from tkinter import messagebox
import sqlite3

# FUNCTIONS

# BBDD
def exitMessage():
    value = messagebox.askquestion("Exit", "Are you sure you want to exit?")

    if value == "yes":
        root.destroy()
    else:
        None

def createNewBBDD():
    try:
        newConnection = sqlite3.connect("BBDD")
        mainCursor = newConnection.cursor()
        mainCursor.execute("CREATE TABLE USERDATA (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME VARCHAR(50), SURNAME VARCHAR(50), PASSWORD VARCHAR(10), ADRESS VARCHAR(50), COMMENTS VARCHAR(100))")
        newConnection.close()

        messagebox.showinfo("Info", "The data base has been created.")

    except sqlite3.OperationalError:
        messagebox.showwarning("Warning","The data base already exist!")

# extra
def clearValues():

    nameEntry.delete(0, END)
    surnameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    adressEntry.delete(0, END)

    commentsBlock.delete(1.0, END)
def creditsMessage():
    messagebox.showinfo("Credits", "All credits to Pildoras and me :D")
def aboutUsMessage():
    messagebox.showinfo("About CRUD", "This application is designed to function as a tool to manipulate user data in a local data base.")

# CRUD
def createBBDDData():
    userData = [
        (userName.get(), userSurname.get(), userPassword.get(), userAdress.get(), commentsBlock.get("1.0", "end-1c"))
    ]

    if userName.get() == '':
        messagebox.showwarning("Warning", "You need at least a name to proceed.")
    else:
        if userID.get() != '':
            messagebox.showwarning("Warning", "You can't put an ID to create a user data.")
        else:
            try:
                newConnection = sqlite3.connect("BBDD")
                mainCursor = newConnection.cursor()
                mainCursor.executemany("INSERT INTO USERDATA VALUES (NULL, ?, ?, ?, ?, ?)", userData)
                newConnection.commit()
                newConnection.close()
        
                messagebox.showinfo("Info", "The data has been saved.")

            except sqlite3.OperationalError:
                messagebox.showwarning("Warning", "First connect to a BBDD.")

            except sqlite3.IntegrityError:
                messagebox.showwarning("Warning", "This ID already exist! Please write another one")

def readBBDDDData():
    try:
        newConnection = sqlite3.connect("BBDD")
        mainCursor = newConnection.cursor()
        mainCursor.execute("SELECT * FROM USERDATA WHERE ID = (?)", userID.get())
        allData = mainCursor.fetchall()

        if allData == []:
            messagebox.showwarning("Warning", "There's no such data in the table!")
        else:
            None

        nameEntry.delete(0, END)
        surnameEntry.delete(0, END)
        passwordEntry.delete(0, END)
        adressEntry.delete(0, END)

        commentsBlock.delete(1.0, END)

        for data in allData:

            nameEntry.insert(0, data[1])
            surnameEntry.insert(0, data[2])
            passwordEntry.insert(0, data[3])
            adressEntry.insert(0, data[4])
            commentsBlock.insert(INSERT, data[5])
        
        newConnection.close()

    except sqlite3.OperationalError:
        messagebox.showwarning("Warning", "First connect to a BBDD.")
    
    except sqlite3.ProgrammingError:
        messagebox.showwarning("Warning", "ID reference is needed.")

def editBBDDData():
    try:
        newConnection = sqlite3.connect("BBDD")
        mainCursor = newConnection.cursor()
        mainCursor.execute("SELECT * FROM USERDATA WHERE ID = (?)", userID.get())
        allData = mainCursor.fetchall()

        if allData == []:
            messagebox.showwarning("Warning", "There's no such data in the table!")
        else:
            None

        userDataChecker = [
            (userName.get()), (userSurname.get()), (userPassword.get()), (userAdress.get()), (commentsBlock.get("1.0", "end-1c"))
        ]

        if userDataChecker == ['', '', '', '', '']:
            messagebox.showwarning("Warning", "To proceed you need at least fill one entry.")
        else:
            userData = [
                (userName.get()), (userSurname.get()), (userPassword.get()), (userAdress.get()), (commentsBlock.get("1.0", "end-1c")), (userID.get())
            ]

            mainCursor.execute("UPDATE USERDATA SET USERNAME = (?), SURNAME = (?), PASSWORD = (?), ADRESS = (?), COMMENTS = (?) WHERE ID = (?)", userData)
            newConnection.commit()
            newConnection.close()

            messagebox.showinfo("Info", "The data has been saved.")

    except sqlite3.OperationalError:
        messagebox.showwarning("Warning", "First connect to a BBDD.")

    except sqlite3.ProgrammingError:
        messagebox.showwarning("Warning", "ID reference is needed.")

def deleteBBDDData():
    try:
        newConnection = sqlite3.connect("BBDD")
        mainCursor = newConnection.cursor()
        mainCursor.execute("SELECT * FROM USERDATA WHERE ID = (?)", userID.get())
        allData = mainCursor.fetchall()

        if allData == []:
            messagebox.showwarning("Warning", "There's no such data in the table!")
        else:
        
            value = messagebox.askquestion("Exit", "Are you sure you want to delete this user data?")

            if value == "yes":
               
                mainCursor.execute("DELETE FROM USERDATA WHERE ID = (?)", userID.get())
                newConnection.commit()
                newConnection.close()

                messagebox.showinfo("Info", "The data has been deleted.")

                nameEntry.delete(0, END)
                surnameEntry.delete(0, END)
                passwordEntry.delete(0, END)
                adressEntry.delete(0, END)

                commentsBlock.delete(1.0, END)
            else:
                None

    except sqlite3.OperationalError:
        messagebox.showwarning("Warning", "First connect to a BBDD.")

    except sqlite3.ProgrammingError:
        messagebox.showwarning("Warning", "ID reference is needed.")

#ROOT
root = Tk()

root.title("CRUD")
root.resizable(False, False)
root.geometry("260x400")
root.iconbitmap("BBDD.ico")

#VARIABLES
userID = StringVar()
userName = StringVar()
userSurname = StringVar()
userPassword = StringVar()
userAdress = StringVar()

#FRAME
mainFrame = Frame(root)
mainFrame.pack(fill=BOTH, expand=True)
mainFrame.config(bg="white")

#MENU
mainMenu = Menu(root)

root.config(menu=mainMenu)

#menu option file
bbddFilemenu = Menu(mainMenu, tearoff=0)
bbddFilemenu.add_command(label="Connect", command=createNewBBDD)
bbddFilemenu.add_command(label="Exit", command=exitMessage)
bbddFilemenu.config(bg="white")

cleanFilemenu = Menu(mainMenu, tearoff=0)
cleanFilemenu.add_command(label="Clean Values", command=clearValues)
cleanFilemenu.config(bg="white")

CRUDFilemenu = Menu(mainMenu, tearoff=0)
CRUDFilemenu.add_command(label="Create", command=createBBDDData)
CRUDFilemenu.add_command(label="Read", command=readBBDDDData)
CRUDFilemenu.add_command(label="Update", command=editBBDDData)
CRUDFilemenu.add_command(label="Delete", command=deleteBBDDData)
CRUDFilemenu.config(bg="white")

helpFilemenu = Menu(mainMenu, tearoff=0)
helpFilemenu.add_command(label="Credits", command=creditsMessage)
helpFilemenu.add_command(label="About CRUD", command=aboutUsMessage)
helpFilemenu.config(bg="white")

#menu option
mainMenu.add_cascade(label="BBDD", menu=bbddFilemenu)
mainMenu.add_cascade(label="Clean", menu=cleanFilemenu)
mainMenu.add_cascade(label="CRUD", menu=CRUDFilemenu)
mainMenu.add_cascade(label="Help", menu=helpFilemenu)

#TEXT LABELS
IDLabel = Label(mainFrame, width=5, anchor="e", text="ID:")
IDLabel.grid(row=0, column=0, padx=10, pady=10, ipadx=15)
IDLabel.config(bg="white")

nameLabel = Label(mainFrame, width=5, anchor="e", text="Name:")
nameLabel.grid(row=1, column=0, padx=10, pady=10, ipadx=15)
nameLabel.config(bg="white")

surnameLabel = Label(mainFrame, width=5, anchor="e", text="Surname:")
surnameLabel.grid(row=2, column=0, padx=10, pady=10, ipadx=15)
surnameLabel.config(bg="white")

passwordLabel = Label(mainFrame, width=5, anchor="e", text="Password:")
passwordLabel.grid(row=3, column=0, padx=10, pady=10, ipadx=15)
passwordLabel.config(bg="white")

adressLabel = Label(mainFrame, width=5, anchor="e", text="Adress:")
adressLabel.grid(row=4, column=0, padx=10, pady=10, ipadx=15)
adressLabel.config(bg="white")

commentsLabel = Label(mainFrame, width=5, anchor="e", text="Comments:")
commentsLabel.grid(row=5, column=0, padx=10, pady=10, ipadx=15)
commentsLabel.config(bg="white")

#TEXT ENTRIES
IDEntry = Entry(mainFrame, textvariable=userID)
IDEntry.grid(row=0, column=1, ipadx=15, columnspan=3)
IDEntry.config(relief="solid")

nameEntry = Entry(mainFrame, textvariable=userName)
nameEntry.grid(row=1, column=1, ipadx=15, columnspan=3)
nameEntry.config(relief="solid")

surnameEntry = Entry(mainFrame, textvariable=userSurname)
surnameEntry.grid(row=2, column=1, ipadx=15, columnspan=3)
surnameEntry.config(relief="solid")

passwordEntry = Entry(mainFrame, show="*", textvariable=userPassword)
passwordEntry.grid(row=3, column=1, ipadx=15, columnspan=3)
passwordEntry.config(relief="solid")

adressEntry = Entry(mainFrame, textvariable=userAdress)
adressEntry.grid(row=4, column=1, ipadx=15, columnspan=3)
adressEntry.config(relief="solid")

commentsBlock = Text(mainFrame, width=19, height=5)
commentsBlock.grid(row=5, column=1, pady=10, columnspan=3)
commentsEntryScrollbar = Scrollbar(mainFrame, command=commentsBlock.yview)
commentsEntryScrollbar.grid(row=6, column=1, ipady=16, sticky="E", columnspan=3)
commentsBlock.config(yscrollcommand=commentsEntryScrollbar.set, relief="solid")

#BUTTONS
createButton = Button(mainFrame, width=6, text="Create", command=createBBDDData)
createButton.grid(row=6, column=0, pady=20)
createButton.config(bg="white", bd=1)

readButton = Button(mainFrame, width=5, text="Read", command=readBBDDDData)
readButton.grid(row=6, column=1, padx=5, pady=20)
readButton.config(bg="white", bd=1, )

updateButton = Button(mainFrame, width=5, text="Update", command=editBBDDData)
updateButton.grid(row=6, column=2, padx=5, pady=20)
updateButton.config(bg="white", bd=1)

deleteButton = Button(mainFrame, width=5, text="Delete", command=deleteBBDDData)
deleteButton.grid(row=6, column=3, padx=5, pady=20)
deleteButton.config(bg="white", bd=1)

# PROGRAM LOOP
root.mainloop()