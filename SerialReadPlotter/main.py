import random
import matplotlib.animation as animation
from threading import *
from matplotlib import *
from tkinter import *
from serial import *
from serial.tools import list_ports
from itertools import count
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

root = Tk()
w = 700
h = 550
root.geometry(str(w) + "x" + str(h))
root.title('datalogger')
root.option_add('*Font', 30)
root.resizable(False, False)
root.overrideredirect(False)

enu = 0
index = count()
xList = []
yList1 = []
yList2 = []
yList3 = []
yList4 = []
myValnew = [0.00] * 4
plotData = 0
status = 0


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
    global plotData
    global status
    global ani
    for i in listB.curselection():
        selectedItem = listB.get(i)
        selectedPort = selectedItem[3]
        print(listB.get(i))
        print(selectedPort)

    ser = Serial(
        "COM" + selectedPort,
        9600,
        timeout=0.05
    )
    status = 1

    myplot = FigureCanvasTkAgg(figure, canvas)
    toolbar = NavigationToolbar2Tk(myplot, canvas)
    toolbar.update()
    myplot.draw()
    myplot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    ani = animation.FuncAnimation(figure, animate, interval=1000)


#     root.after(100, Thread(target=readSerial).start)
#
#
# def readSerial():
#     global enu
#     global myValnew
#     global ani
#     myVal = ser.readline()
#     enu = 1 + enu
#     myVal = str(myVal)
#     myVal = myVal.replace('\\r\\n', "")
#     myVal = myVal.replace('b', "")
#     myVal = myVal.replace('\'', "")
#     myValnew = myVal.split(',')
#     try:
#         print(myValnew[0], myValnew[1], myValnew[2], myValnew[3])
#
#     except:
#         pass
#
#     Tvalu.config(text=myVal)
#     root.after(1000, Thread(target=readSerial).start)


def animate(i):
    global myValnew
    myVal = ser.readline()
    myVal = str(myVal)
    myVal = myVal.replace('\\r\\n', "")
    myVal = myVal.replace('b', "")
    myVal = myVal.replace('\'', "")
    myValnew = myVal.split(',')
    try:
        xList.append(next(index))
        yList1.append(int(myValnew[0]))
        yList2.append(int(myValnew[1]))
        yList3.append(int(myValnew[2]))
        yList4.append(int(myValnew[3]))
        print(i, int(myValnew[0]), int(myValnew[1]), int(myValnew[2]), int(myValnew[3]))
        Tvalu.config(text=myVal)

        a.plot(xList, yList1, color='orange')

    except:
        pass


F1 = Frame(root, height=h, width=w, bg='#5C6592')
listB = Listbox(F1, width=50, height=3)
canvas = Canvas(F1, height=310, width=655, bg='#ffffff')

TconsValue = Label(F1, text="nilai:", font=("Arial", 32), bg='#5C6592', fg='#ffffff')
Tvalu = Label(F1, font=("Arial", 32), bg='#5C6592', fg='#ffffff')

Bscan = Button(F1, text="Scan", width=6, height=1, command=scanSerial)
Bconn = Button(F1, text="Connect", width=8, height=1, command=connectSerial)

F1.place(y=0, x=0)
Bscan.place(y=20, x=510)
Bconn.place(y=20, x=600)
TconsValue.place(y=130, x=20)
Tvalu.place(y=130, x=150)
listB.place(y=20, x=20)

canvas.place(y=200, x=20)

figure = Figure(figsize=(6.63, 2.5), dpi=100)
a = figure.add_subplot(111)

root.mainloop()
