import sqlite3
import random
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
con = sqlite3.connect("Apple.db")
con.execute("PRAGMA foreign_keys=ON;")
cur = con.cursor()
row_num = 1
ROOM_TYPE = ["Suite","Luxury","Studio"]
TABLES = ["Guest_info","Rooms","Reservations","Invoice"]

table_creation = ["CREATE TABLE IF NOT EXISTS Guest_info(Guest_Id INTEGER PRIMARY KEY, First_Name TEXT NOT NULL, Last_Name TEXT NOT NULL, Email CHAR(100) UNIQUE NOT NULL, Phone_No CHAR(10) UNIQUE NOT NULL) "
                  ,"CREATE TABLE IF NOT EXISTS Rooms(Room_Num INTEGER Primary Key,Status BOOLEAN NOT NULL, Room_type TEXT NOT NULL)"
                  , "CREATE TABLE IF NOT EXISTS Reservations(Reservation_ID INTEGER PRIMARY KEY, Room INTEGER NOT NULL, Guest INTEGER NOT NULL, CHECK_IN DATETIME NOT NULL, CHECK_OUT DATETIME NOT NULL, FOREIGN KEY (Room) REFERENCES Rooms(Room_Num), FOREIGN KEY (Guest) REFERENCES Guest_info(Guest_Id))"
                  , "CREATE TABLE IF NOT EXISTS Invoice(Invoice_ID INTEGER PRIMARY KEY, Reservation_ID TINYINT NOT NULL, Item TEXT NOT NULL, Quantity INTEGER NOT NULL, Price FLOAT NOT NULL, Date DATE NOT NULL, FOREIGN KEY (Reservation_ID) REFERENCES Reservations(Reservation_ID))"]

def query_execute(query, params):
    cur.execute(query, params)
    con.commit()

for i in table_creation:
    cur.execute(i)
if len(cur.execute("SELECT * FROM Rooms").fetchall()) < 50:
    for i in range(50):
        cur.execute("INSERT INTO Rooms(Status, Room_type) VALUES (?,?)",(0,random.choice(ROOM_TYPE)))


window = Tk()
window.title("Hotel Database")
frame = Frame(window)
frame.pack(fill=BOTH, expand=1)

canvas = Canvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar_x = ttk.Scrollbar(window, orient='horizontal', command=canvas.xview)
scrollbar_x.pack(side=BOTTOM, fill=X)

scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
scrollbar_y.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar_y.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

second_frame = Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw")

#Display Data


def display():
    global row_num
    row_num=1
    t1 = "Reservation ID"
    t2 = "Room Number"
    t3 = "Guest ID"
    t4 = "Check In"
    t5 = "Check Out"
    Label(second_frame,text = t1,font=("Arial",20,"bold")).grid(row=0,column=0,)
    Label(second_frame,text = t2,font=("Arial",20,"bold")).grid(row=0,column=1,padx=5)
    Label(second_frame,text = t3,font=("Arial",20,"bold")).grid(row=0,column=2,padx=5)
    Label(second_frame,text = t4,font=("Arial",20,"bold")).grid(row=0,column=3,padx=5)
    Label(second_frame,text = t5,font=("Arial",20,"bold")).grid(row=0,column=4,padx=5)
    data = cur.execute(f"SELECT * FROM Reservations")
    data = data.fetchall()
    data = list(data)
    for row in data:
        FONTSIZE = 24
        FONT = "Arial"
        t1 = str(row[0])
        t2 = str(row[1])
        t3 = str(row[2])
        t4 = str(row[3])
        t5 = str(row[4])
        Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
        Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
        Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
        Label(second_frame,text = t4,font=(FONT,FONTSIZE)).grid(row=row_num,column=3)
        Label(second_frame,text = t5,font=(FONT,FONTSIZE)).grid(row=row_num,column=4)
        row_num+=1
        
display()
      
# Allowing for Data Entry
def add_reservation():
    try:
        global row_num
        r1=r.get()
        g1=g.get()
        i1=i.get()
        o1=o.get()
        if "" in [r1,g1,i1,o1]:
            raise ValueError()
        query_execute('INSERT INTO Reservations(Room, Guest, CHECK_IN, CHECK_OUT) VALUES (?,?,?,?)',(r1,g1,i1,o1))
        data = cur.execute(f"SELECT * FROM RESERVATIONS WHERE Reservation_ID = {row_num}").fetchall()
        FONTSIZE = 20
        FONT = "Arial"
        t1 = str(data[0][0])
        t2 = str(data[0][1])
        t3 = str(data[0][2])
        t4 = str(data[0][3])
        t5 = str(data[0][4])
        Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
        Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
        Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
        Label(second_frame,text = t4,font=(FONT,FONTSIZE)).grid(row=row_num,column=3)
        Label(second_frame,text = t5,font=(FONT,FONTSIZE)).grid(row=row_num,column=4)
        row_num+=1
        print(data[0])
        r.grid_remove()
        g.grid_remove()
        i.grid_remove()
        o.grid_remove()
        add_button.grid_remove()
        re.grid_remove()
        u.grid_remove()
        r2.grid_remove()
        g2.grid_remove()
        i2.grid_remove()
        o2.grid_remove()
        update_button.grid_remove()
        Room_Table.grid_remove()
        Guest_Table.grid_remove()
        Invoice_Table.grid_remove()
        delete_button.grid_remove()
        r.grid(row = row_num+1,column=1,padx=4)
        g.grid(row=row_num+1,column=2,padx=4)
        i.grid(row=row_num+1,column=3,padx=4)
        o.grid(row=row_num+1,column=4,padx=4)
        add_button.grid(row=row_num+1,column=5)
        u.grid(row=row_num+2,column=0,padx=4,pady=10)
        r2.grid(row=row_num+2,column=1,padx=4,pady=10)
        i2.grid(row=row_num+2,column=2,padx=4,pady=10)
        g2.grid(row=row_num+2,column=3,padx=4,pady=10)
        o2.grid(row=row_num+2,column=4,padx=4,pady=10)
        update_button.grid(row=row_num+2,column=5,padx=4,pady=10)
        re.grid(row=row_num+3,column=0,pady=20)
        delete_button.grid(row=row_num+3,column=5,padx=4,pady=20)
        Invoice_Table.grid(row=row_num+4,column=1)
        Room_Table.grid(row=row_num+4,column=2)
        Guest_Table.grid(row=row_num+4,column=3)
        r.delete(0,END)
        g.delete(0,END)
        i.delete(0,END)
        o.delete(0,END)
        con.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror(message="Guest ID or Room Number is/are Incorrect")
    except:
        messagebox.showerror(message="All Fields Need to be Filled")
FONT = "Arial"
FONTSIZE = 20
r = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
r.grid(row = row_num+1,column=1,padx=4)
g = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
g.grid(row=row_num+1,column=2,padx=4)
i = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
i.grid(row=row_num+1,column=3,padx=4)
o = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
o.grid(row=row_num+1,column=4,padx=4)

add_button = Button(second_frame,text="Add",command=add_reservation,font=(FONT,FONTSIZE))
add_button.grid(row=row_num+1,column=5,padx=4)

#Allowing for Data Update
def update():
    try:
        cur.execute('UPDATE Reservations SET Room = ?,Guest = ?, CHECK_IN = ?, CHECK_OUT = ? WHERE Reservation_ID = ?',(r2.get(),g2.get(),i2.get(),o2.get(),u.get()))
        for i in second_frame.winfo_children():
            if type(i)==type(Label()):
                i.destroy()
        display()
    except sqlite3.IntegrityError:
        messagebox.showerror(message="Guest ID or Room Number is/are Incorrect")
    except:
        messagebox.showerror(message="All Fields Need to be Filled")
u = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
u.grid(row=row_num+2,column=0,padx=4,pady=10)
r2 = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
r2.grid(row = row_num+2,column=1,padx=4,pady=10)
g2 = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
g2.grid(row=row_num+2,column=2,padx=4,pady=10)
i2 = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
i2.grid(row=row_num+2,column=3,padx=4,pady=10)
o2 = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
o2.grid(row=row_num+2,column=4,padx=4,pady=10)
update_button = Button(second_frame,text="Update",pady=10,command=update,font=(FONT,FONTSIZE))
update_button.grid(row=row_num+2,column=5,pady=10,padx=4)


#Allowing for Data Deletion
re = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
re.grid(row=row_num+3,column=0,pady=10)

def delete_reservation():
    try:
        query_execute("DELETE FROM Reservations WHERE Reservation_ID=?",re.get())
        for i in second_frame.winfo_children():
            if type(i)==type(Label()):
                i.destroy()
        global row_num
        row_num=1
        display()
        con.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror(message="Guest ID or Room Number is/are Incorrect")
    except:
        messagebox.showerror(message="All Fields Need to be Filled")



delete_button = Button(second_frame,text="Delete",command=delete_reservation,font=(FONT,FONTSIZE))
delete_button.grid(row=row_num+3,column=5,padx=4,pady=20)


#display other tables
def display_room():
    room_win = Toplevel()
    frame = Frame(room_win)
    frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar_x = ttk.Scrollbar(room_win, orient='horizontal', command=canvas.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)

    scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollbar_y.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")
    room_win.title("Room")
    data = cur.execute(f"SELECT * FROM Rooms")
    data = data.fetchall()
    data = list(data)
    row_num=1
    FONTSIZE = 20
    FONT = "Arial"
    Label(second_frame,text="Room Number",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=0,padx=10)
    Label(second_frame,text="Status",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=1,padx=10)
    Label(second_frame,text="Room Type",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=2,padx=10)
    for row in data:       
        t1 = str(row[0])
        t2 = str(row[1])
        t3 = str(row[2])
        Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
        Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
        Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
        row_num+=1
    def add_room():
        try:
            nonlocal row_num
            r1=r.get()
            g1=g.get()
            if "" in [r1,g1]:
                raise ValueError()
            query_execute('INSERT INTO Rooms(Status,Room_type) VALUES (?,?)',(r1,g1))
            data = cur.execute(f"SELECT * FROM Rooms WHERE Room_Num = {row_num}").fetchall()
            FONTSIZE = 20
            FONT = "Arial"
            print(data)
            t1 = str(data[0][0])
            t2 = str(data[0][1])
            t3 = str(data[0][2])
            Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
            Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
            Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
            row_num+=1
            print(data[0])
            r.grid_remove()
            g.grid_remove()
            add_button.grid_remove()
            re.grid_remove()
            delete_button.grid_remove()
            r.grid(row = row_num+1,column=1,padx=4)
            g.grid(row=row_num+1,column=2,padx=4)
            add_button.grid(row=row_num+1,column=5)
            re.grid(row=row_num+2,column=0,pady=20)
            delete_button.grid(row=row_num+2,column=3,padx=4,pady=20)
            r.delete(0,END)
            g.delete(0,END)
            con.commit()
        except :
            messagebox.showerror(second_frame,message="All Fields Need to be Filled")
    FONT = "Arial"
    FONTSIZE = 20
    r = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    r.grid(row = row_num+1,column=1,padx=4)
    g = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    g.grid(row=row_num+1,column=2,padx=4)
    add_button = Button(second_frame,text="Add",command=add_room,font=(FONT,FONTSIZE))
    add_button.grid(row=row_num+1,column=3,padx=4)
    re = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    re.grid(row=row_num+2,column=0,pady=20)

    def delete_room():
        try:
            print(re.get())
            query_execute("DELETE FROM Rooms WHERE Room_Num=?",(re.get(),))
            room_win.destroy()
            display_room()
            con.commit()
        except:
            messagebox.showerror(message="All Fields Need to be Filled")
            
    delete_button = Button(second_frame,text="Delete",command=delete_room,font=(FONT,FONTSIZE))
    delete_button.grid(row=row_num+2,column=3,padx=4,pady=20)

def display_guest():
    room_win = Toplevel()
    room_win.title("Guest")
    frame = Frame(room_win)
    frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar_x = ttk.Scrollbar(room_win, orient='horizontal', command=canvas.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)

    scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollbar_y.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")
    
    FONT = "Arial"
    FONTSIZE = 20
    Label(second_frame,text = "Guest ID",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=0,padx=4)
    Label(second_frame,text = "First Name",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=1)
    Label(second_frame,text = "Last Name",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=2)
    Label(second_frame,text = "Email",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=3)
    Label(second_frame,text = "Phone No.",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=4)
    
    data = cur.execute(f"SELECT * FROM Guest_info")
    data = data.fetchall()
    data = list(data)
    row_num=1
    for row in data:       
        FONTSIZE = 20
        FONT = "Arial"
        t1 = str(row[0])
        t2 = str(row[1])
        t3 = str(row[2])
        t4 = str(row[3])
        t5 = str(row[4])
        Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
        Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
        Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
        Label(second_frame,text = t4,font=(FONT,FONTSIZE)).grid(row=row_num,column=3)
        Label(second_frame,text = t5,font=(FONT,FONTSIZE)).grid(row=row_num,column=4)
        row_num+=1

    def add_guest():
        try:
            nonlocal row_num
            r1=r.get()
            g1=g.get()
            i1=i.get()
            o1=o.get()
            if "" in [r1,g1,i1,o1]:
                raise ValueError()
            query_execute('INSERT INTO Guest_info(First_Name, Last_Name, Email, Phone_No) VALUES (?,?,?,?)',(r1,g1,i1,o1))
            data = cur.execute(f"SELECT * FROM Guest_info WHERE Guest_Id = {row_num}").fetchall()
            FONTSIZE = 20
            FONT = "Arial"
            t1 = str(data[0][0])
            t2 = str(data[0][1])
            t3 = str(data[0][2])
            t4 = str(data[0][3])
            t5 = str(data[0][4])
            Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
            Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1,padx=4)
            Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2,padx=4)
            Label(second_frame,text = t4,font=(FONT,FONTSIZE)).grid(row=row_num,column=3,padx=4)
            Label(second_frame,text = t5,font=(FONT,FONTSIZE)).grid(row=row_num,column=4,padx=4)
            row_num+=1
            print(data[0])
            r.grid_remove()
            g.grid_remove()
            i.grid_remove()
            o.grid_remove()
            add_button.grid_remove()
            re.grid_remove()
            delete_button.grid_remove()
            r.grid(row = row_num+1,column=1,padx=4)
            g.grid(row=row_num+1,column=2,padx=4)
            i.grid(row=row_num+1,column=3,padx=4)
            o.grid(row=row_num+1,column=4,padx=4)
            add_button.grid(row=row_num+1,column=5)
            re.grid(row=row_num+2,column=0,pady=20)
            delete_button.grid(row=row_num+2,column=5,padx=4,pady=20)
            r.delete(0,END)
            g.delete(0,END)
            i.delete(0,END)
            o.delete(0,END)
            con.commit()
        except:
            messagebox.showerror(message="All Fields Need to be Filled")
    FONT = "Arial"
    FONTSIZE = 20
    r = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    r.grid(row = row_num+1,column=1,padx=4)
    g = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    g.grid(row=row_num+1,column=2,padx=4)
    i = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    i.grid(row=row_num+1,column=3,padx=4)
    o = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    o.grid(row=row_num+1,column=4,padx=4)

    add_button = Button(second_frame,text="Add",command=add_guest,font=(FONT,FONTSIZE))
    add_button.grid(row=row_num+1,column=5,padx=4)
    re = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    re.grid(row=row_num+2,column=0,pady=20)
    def delete_guest():
        try:
            print(re.get())
            query_execute("DELETE FROM Guest_info WHERE Guest_Id=?",(re.get(),))
            room_win.destroy()
            display_guest()
            con.commit()
        except:
            messagebox.showerror(message="All Fields Need to be Filled")

    delete_button = Button(second_frame,text="Delete",command=delete_guest,font=(FONT,FONTSIZE))
    delete_button.grid(row=row_num+2,column=5,padx=4,pady=20)

def display_invoice():
    room_win = Toplevel()
    room_win.title("Invoice")
    frame = Frame(room_win)
    frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar_x = ttk.Scrollbar(room_win, orient='horizontal', command=canvas.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)

    scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollbar_y.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")
    data = cur.execute(f"SELECT * FROM Invoice")
    data = data.fetchall()
    data = list(data)
    row_num=1
    FONTSIZE = 20
    FONT = "Arial"
    Label(second_frame,text = "Invoice ID",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=0,padx=4)
    Label(second_frame,text = "Reservation ID",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=1)
    Label(second_frame,text = "Item Name",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=2)
    Label(second_frame,text = "Quantity",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=3)
    Label(second_frame,text = "Total Price",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=4)
    Label(second_frame,text = "Date",font=(FONT,FONTSIZE,"bold")).grid(row=0,column=5)
    for row in data:
        t1 = str(row[0])
        t2 = str(row[1])
        t3 = str(row[2])
        t4 = str(row[3])
        t5 = str(row[4])
        t6 = str(row[5])
        Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
        Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
        Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
        Label(second_frame,text = t4,font=(FONT,FONTSIZE)).grid(row=row_num,column=3)
        Label(second_frame,text = t5,font=(FONT,FONTSIZE)).grid(row=row_num,column=4)
        Label(second_frame,text = t6,font=(FONT,FONTSIZE)).grid(row=row_num,column=5)
        row_num+=1


    def add_invoice():
        try:
            nonlocal row_num
            r1=r.get()
            g1=g.get()
            i1=i.get()
            o1 = o.get()
            j1 = j.get()
            if "" in [r1,g1,i1,o1,j1]:
                raise ValueError()
            query_execute('INSERT INTO Invoice(Reservation_ID, Item, Quantity, Price, Date) VALUES (?,?,?,?,?)',(r1,g1,i1,o1,j1))
            data = cur.execute(f"SELECT * FROM Invoice WHERE Invoice_ID = {row_num}").fetchall()
            FONTSIZE = 20
            FONT = "Arial"
            t1 = str(data[0][0])
            t2 = str(data[0][1])
            t3 = str(data[0][2])
            t4 = str(data[0][3])
            t5 = str(data[0][4])
            t6 = str(data[0][5])
            Label(second_frame,text = t1,font=(FONT,FONTSIZE)).grid(row=row_num,column=0,padx=4)
            Label(second_frame,text = t2,font=(FONT,FONTSIZE)).grid(row=row_num,column=1)
            Label(second_frame,text = t3,font=(FONT,FONTSIZE)).grid(row=row_num,column=2)
            Label(second_frame,text = t4,font=(FONT,FONTSIZE)).grid(row=row_num,column=3)
            Label(second_frame,text = t5,font=(FONT,FONTSIZE)).grid(row=row_num,column=4)
            Label(second_frame,text = t6,font=(FONT,FONTSIZE)).grid(row=row_num,column=5)
            row_num+=1
            print(data[0])
            r.grid_remove()
            g.grid_remove()
            i.grid_remove()
            o.grid_remove()
            j.grid_remove()
            add_button.grid_remove()
            re.grid_remove()
            delete_button.grid_remove()
            r.grid(row = row_num+1,column=1,padx=4)
            g.grid(row=row_num+1,column=2,padx=4)
            i.grid(row=row_num+1,column=3,padx=4)
            o.grid(row=row_num+1,column=4,padx=4)
            j.grid(row=row_num+1,column=5,padx=4)
            add_button.grid(row=row_num+1,column=6)
            re.grid(row=row_num+2,column=0,pady=20)
            delete_button.grid(row=row_num+2,column=6,padx=4,pady=20)
            r.delete(0,END)
            g.delete(0,END)
            i.delete(0,END)
            o.delete(0,END)
            j.delete(0,END)
            con.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror(second_frame,message="Reservation ID is Incorrect")
        except:
            messagebox.showerror(second_frame,message="All Fields Need to be Filled")
    FONT = "Arial"
    FONTSIZE = 20
    r = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    r.grid(row = row_num+1,column=1,padx=4)
    g = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    g.grid(row=row_num+1,column=2,padx=4)
    i = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    i.grid(row=row_num+1,column=3,padx=4)
    o = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    o.grid(row=row_num+1,column=4,padx=4)
    j = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    j.grid(row=row_num+1,column=5,padx=4)
    add_button = Button(second_frame,text="Add",command=add_invoice,font=(FONT,FONTSIZE))
    add_button.grid(row=row_num+1,column=6,padx=4)
    def delete_guest():
        try:
            print(re.get())
            query_execute("DELETE FROM Invoice WHERE Invoice_Id=?",(re.get(),))
            room_win.destroy()
            display_invoice()
            con.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror(second_frame,message="Reservation ID is Incorrect")
        except:
            messagebox.showerror(second_frame,message="All Fields Need to be Filled")
    re = Entry(second_frame,width=10,font=(FONT,FONTSIZE))
    re.grid(row=row_num+2,column=0,pady=20)
    delete_button = Button(second_frame,text="Delete",command=delete_guest,font=(FONT,FONTSIZE))
    delete_button.grid(row=row_num+2,column=5,padx=4,pady=20)
    
    
Room_Table = Button(second_frame,text="Switch to Rooms Table",command=display_room,font=(FONT,16))
Room_Table.grid(row=row_num+4,column=1,padx=10)

Guest_Table = Button(second_frame,text="Switch to Guest Table",command=display_guest,font=(FONT,16))
Guest_Table.grid(row=row_num+4,column=2,padx=10)
Invoice_Table = Button(second_frame,text="Switch to Invoice Table",command=display_invoice,font=(FONT,16))
Invoice_Table.grid(row=row_num+4,column=3,padx=10)

window.mainloop()




for i in TABLES:
    query = f"DROP TABLE {i}"
    cur.execute(query)


con.commit()
con.close()