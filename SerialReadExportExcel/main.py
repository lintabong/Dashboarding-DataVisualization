import serial
from serial.tools import list_ports
import tkinter as tk
import os
import pandas
import xlsxwriter
from time import sleep
import threading

root = tk.Tk()
w = 400
h = 300
root.geometry(str(w) + "x" + str(h))
root.title('datalogger')
root.option_add('*Font', 30)
root.resizable(False, False)
root.overrideredirect(False)

enu = 0

data = {
    "x1": [],
    "x2": [],
    "x3": []
}

df1 = pandas.DataFrame(data)


def scanSerial():
    listB.delete(0, 10)
    myList = list_ports.comports()
    n = 0
    for serialReady in myList:
        n = n + 1
        print(n, serialReady)
        listB.insert(n, serialReady)

    print(type(myList))


def connectSerial():
    global ser
    global selectedPort
    for i in listB.curselection():
        selectedItem = listB.get(i)
        selectedPort = selectedItem[3]
        print(listB.get(i))
        print(selectedPort)

    ser = serial.Serial(
        "COM" + selectedPort,
        9600,
        timeout=0.05
    )
    root.after(3000, threading.Thread(target=readSerial).start)


def readSerial():
    global ser
    global enu
    global df1
    myVal = ser.readline()
    enu = 1 + enu
    myVal = str(myVal)
    myVal = myVal.replace('\\r\\n', "")
    myVal = myVal.replace('b', "")
    myVal = myVal.replace('\'', "")
    myValnew = myVal.split(',')
    try:
        print(myValnew[0], myValnew[1], myValnew[2])
        add = {
            "x1": [myValnew[0]],
            "x2": [myValnew[1]],
            "x3": [myValnew[2]]
        }

        df2 = pandas.DataFrame(add)
        df1 = df1.append(df2, True)
    except:
        pass

    # print(enu, myValnew, len((myValnew)))
    Tvalu.config(text=myVal)
    root.after(500, threading.Thread(target=readSerial).start)


def printLabel():
    global df1
    print(df1)
    excel_writer = pandas.ExcelWriter('exportData.xlsx', engine='xlsxwriter')
    df1.to_excel(excel_writer, sheet_name='data 1')
    excel_writer.save()


F1 = tk.Frame(root, height=h, width=w, bg='#5C6592')
listB = tk.Listbox(F1)

Tvalu = tk.Label(F1, font=("Arial", 32), bg='#5C6592', fg='#ffffff')

Bscan = tk.Button(F1, text="Scan", width=6, height=1, command=scanSerial)
Bconn = tk.Button(F1, text="Connect", width=8, height=1, command=connectSerial)
Bexpo = tk.Button(F1, text="Export", width=8, height=2, command=printLabel)
Bexit = tk.Button(F1, text="Quit", width=6, height=1, command=quit)

F1.place(y=0, x=0)
Bscan.place(y=20, x=220)
Bconn.place(y=20, x=310)
Bexit.place(y=60, x=310)
Bexpo.place(y=160, x=220)
Tvalu.place(y=230, x=20)
listB.place(y=20, x=20)

root.mainloop()
