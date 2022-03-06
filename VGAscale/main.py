import serial
import os
import threading
import numpy
import tkinter as tk
from time import strftime
from time import sleep
from escpos import *

root = tk.Tk()
w = 900
h = 480

root.geometry(str(w) + "x" + str(h))
root.title('datalogger')
root.option_add('*Font', 30)
root.resizable(False, False)
root.overrideredirect(False)

# init variable
countData = 5000
savedNum = [0] * countData
savedVal = [0.00] * countData
o, p, q, r, s, t = 0, 0, 0, 0, 0, 0

sleep(6)


def shutDown():
    os.system("shutdown now")


def exitGUI():
    global o
    o = o + 1
    if o == 20:
        root.destroy()


def deleData():
    global q
    savedNum[q] = 0
    savedVal[q] = 0.00
    q = q - 1


def nextData():
    global p
    p = p + 14
    print(p)


def prevData():
    global p
    if not p - 14 < 0:
        p = p - 14
    print(p)


def clearData():
    global q
    global s
    for s in range(countData):
        savedNum[s] = 0
        savedVal[s] = 0.00
    q = 0


def time():
    time_utc = strftime("%I:%M:%S %p") + "    " + strftime("%a, %b %d, %Y")
    tDate.config(text=time_utc)
    root.after(1000, time)

d = 0
statusCode = 0
arrbuff = [0.00]*3
def readData():
    global q
    global d
    global statusCode
    global myValnew
    global arrbuff
    try:
        ser = serial.Serial(
            "/dev/ttyUSB0",
            9600,
            timeout=0.05
        )
        myVal = ser.readline()
        myVal = str(myVal)
        myVal = myVal.replace('\\r\\n', "")
        myVal = myVal.replace('b', "")
        myVal = myVal.replace('\'', "")
        myValnew = myVal.split(',')
        tValu.config(text=myValnew[4])

        arrbuff[d] = myValnew[4]

        d = d + 1
        if d == 3:
            d = 0

        if arrbuff[0] == arrbuff[1] == arrbuff[2] and statusCode == 0:
            q = q + 1
            savedNum[q] = q
            savedVal[q] = float(myValnew[0])
            statusCode = 1

        if float(arrbuff[0]) == float(arrbuff[1]) == float(arrbuff[2]) <= 2.00:
            statusCode = 0
        # print(q, float(myValnew[0]))
    except:
        print("not Connected")

    root.after(1000, threading.Thread(target=readData).start)


def printData():
    o = 0
    global myValnew
    for numData in range(countData):
        if not savedVal[numData] == 0:
            o = o + 1
            print(o, savedVal[numData])

    readyPrintData = [0.00] * (o)

    for numData in range(o):
        readyPrintData[i] = savedVal[numData + 1]

    maxVal = numpy.max(readyPrintData)
    minVal = numpy.min(readyPrintData)
    avgVal = numpy.average(readyPrintData)
    sumVal = numpy.sum(readyPrintData)
    stdVal = numpy.std(readyPrintData)
    stdVal1 = (stdVal * r) / (r - 1)

    print(readyPrintData)
    print(o, maxVal, minVal, avgVal, sumVal, stdVal, stdVal1)

    p = printer.File("/dev/ttyUSB1")
    p.text(strftime("%a, %b %d, %Y") + "\n")
    p.text(strftime("%I:%M:%S %p") + "\n")
    p.text("==================================")
    p.text("PRODUCT : " + str(myValnew[2]) + "\n")
    p.text("==================================")
    for numData in range(o):
        print(readyPrintData[numData])
        p.text(numData)
        p.text("               ")
        p.text(str(readyPrintData[numData]) + "kg")
        p.text("\n")

    p.text("N                        " + str(r) + "\n")
    p.text("Max                 " + str(maxVal) + " kg\n")
    p.text("Min                 " + str(minVal) + " kg\n")
    p.text("Ave                 " + str(avgVal) + " kg\n")
    p.text("Sum                 " + str(sumVal) + " kg\n")
    p.text("n                   " + str(stdVal) + " kg\n")
    p.text("n-1                 " + str(stdVal1) + " kg\n")
    p.text("\n")
    p.text("COMP.N" + "\n")
    p.text("HI                         " + "PC" + "\n")
    p.text("GOOD                       " + "PC" + "\n")
    p.text("LO                         " + "PC" + "\n")
    p.text("=================================\n")
    p.text("=================================\n")
    p.cut()
    p.close()


def updateDat():
    num1.config(text=savedNum[p + 1])
    num2.config(text=savedNum[p + 2])
    num3.config(text=savedNum[p + 3])
    num4.config(text=savedNum[p + 4])
    num5.config(text=savedNum[p + 5])
    num6.config(text=savedNum[p + 6])
    num7.config(text=savedNum[p + 7])
    num8.config(text=savedNum[p + 8])
    num9.config(text=savedNum[p + 9])
    num10.config(text=savedNum[p + 10])
    num11.config(text=savedNum[p + 11])
    num12.config(text=savedNum[p + 12])
    num13.config(text=savedNum[p + 13])
    num14.config(text=savedNum[p + 14])

    val1.config(text=savedVal[p + 1])
    val2.config(text=savedVal[p + 2])
    val3.config(text=savedVal[p + 3])
    val4.config(text=savedVal[p + 4])
    val5.config(text=savedVal[p + 5])
    val6.config(text=savedVal[p + 6])
    val7.config(text=savedVal[p + 7])
    val8.config(text=savedVal[p + 8])
    val9.config(text=savedVal[p + 9])
    val10.config(text=savedVal[p + 10])
    val11.config(text=savedVal[p + 11])
    val12.config(text=savedVal[p + 12])
    val13.config(text=savedVal[p + 13])
    val14.config(text=savedVal[p + 14])

    root.after(100, updateDat)


# frame design============================================================
myFrame = tk.Frame(root, height=h, width=w)
fStat1 = tk.Frame(myFrame, height=0.07 * h, width=w, bg='#000000')
fStat2 = tk.Frame(myFrame, height=0.15 * h, width=w, bg='#5C6592')
fStat3 = tk.Frame(myFrame, height=0.63 * h, width=w, bg='#B7BDDE')
fStat4 = tk.Frame(myFrame, height=0.15 * h, width=w, bg='#FFFFFF')

for i in [130, 164, 198, 232, 266, 300, 334]:
    tk.Frame(myFrame, height=30, width=60, background='white').place(x=24, y=i)
    tk.Frame(myFrame, height=30, width=(w - 350) / 2, background='white').place(x=88, y=i)

for i in [130, 164, 198, 232, 266, 300, 334]:
    tk.Frame(myFrame, height=30, width=60, background='white').place(x=454, y=i)
    tk.Frame(myFrame, height=30, width=(w - 400) / 2, background='white').place(x=518, y=i)
# =======================================================================

# object text============================================================
tDate = tk.Label(myFrame, bg='#000000', fg='white')
tStat = tk.Label(myFrame, text="Statistic", font=("Arial", 32), bg='#5C6592', fg='white')
tWeig = tk.Label(myFrame, text="Weight: ", bg='#5C6592', fg='white')
tValu = tk.Label(myFrame, font=("Arial", 20), bg='#5C6592', fg='white')

num1 = tk.Label(myFrame, bg='white', fg='#5C6592')
num2 = tk.Label(myFrame, bg='white', fg='#5C6592')
num3 = tk.Label(myFrame, bg='white', fg='#5C6592')
num4 = tk.Label(myFrame, bg='white', fg='#5C6592')
num5 = tk.Label(myFrame, bg='white', fg='#5C6592')
num6 = tk.Label(myFrame, bg='white', fg='#5C6592')
num7 = tk.Label(myFrame, bg='white', fg='#5C6592')
num8 = tk.Label(myFrame, bg='white', fg='#5C6592')
num9 = tk.Label(myFrame, bg='white', fg='#5C6592')
num10 = tk.Label(myFrame, bg='white', fg='#5C6592')
num11 = tk.Label(myFrame, bg='white', fg='#5C6592')
num12 = tk.Label(myFrame, bg='white', fg='#5C6592')
num13 = tk.Label(myFrame, bg='white', fg='#5C6592')
num14 = tk.Label(myFrame, bg='white', fg='#5C6592')

val1 = tk.Label(myFrame, bg='white', fg='#5C6592')
val2 = tk.Label(myFrame, bg='white', fg='#5C6592')
val3 = tk.Label(myFrame, bg='white', fg='#5C6592')
val4 = tk.Label(myFrame, bg='white', fg='#5C6592')
val5 = tk.Label(myFrame, bg='white', fg='#5C6592')
val6 = tk.Label(myFrame, bg='white', fg='#5C6592')
val7 = tk.Label(myFrame, bg='white', fg='#5C6592')
val8 = tk.Label(myFrame, bg='white', fg='#5C6592')
val9 = tk.Label(myFrame, bg='white', fg='#5C6592')
val10 = tk.Label(myFrame, bg='white', fg='#5C6592')
val11 = tk.Label(myFrame, bg='white', fg='#5C6592')
val12 = tk.Label(myFrame, bg='white', fg='#5C6592')
val13 = tk.Label(myFrame, bg='white', fg='#5C6592')
val14 = tk.Label(myFrame, bg='white', fg='#5C6592')
# =======================================================================

# object button==========================================================
bDele = tk.Button(myFrame, text="delete", width=10, height=1, command=deleData)
bNext = tk.Button(myFrame, text=">>", width=5, height=1, command=nextData)
bPrev = tk.Button(myFrame, text="<<", width=5, height=1, command=prevData)

bClea = tk.Button(myFrame, text="clear", width=10, height=2, command=clearData)
bShut = tk.Button(myFrame, text="Shutdown", width=10, height=2, command=shutDown)
bHome = tk.Button(myFrame, text="Home", width=10, height=2, command=exitGUI)
bPrin = tk.Button(myFrame, text="Print", width=10, height=2, command=printData)
# ========================================================================

myFrame.place(y=0, x=0)
fStat1.place(y=0)
fStat2.place(y=0.07 * h)
fStat3.place(y=0.22 * h)
fStat4.place(y=0.85 * h)
tDate.place(y=7, x=w - 380)

tStat.place(y=40, x=10)
tWeig.place(y=70, x=450)
tValu.place(y=60, x=w - 260)

num1.place(x=24, y=133)
num2.place(x=24, y=167)
num3.place(x=24, y=201)
num4.place(x=24, y=235)
num5.place(x=24, y=269)
num6.place(x=24, y=303)
num7.place(x=24, y=337)
num8.place(x=458, y=133)
num9.place(x=458, y=167)
num10.place(x=458, y=201)
num11.place(x=458, y=235)
num12.place(x=458, y=269)
num13.place(x=458, y=303)
num14.place(x=458, y=337)

val1.place(x=88, y=133)
val2.place(x=88, y=167)
val3.place(x=88, y=201)
val4.place(x=88, y=235)
val5.place(x=88, y=269)
val6.place(x=88, y=303)
val7.place(x=88, y=337)
val8.place(x=528, y=133)
val9.place(x=528, y=167)
val10.place(x=528, y=201)
val11.place(x=528, y=235)
val12.place(x=528, y=269)
val13.place(x=528, y=303)
val14.place(x=528, y=337)

bDele.place(y=h - 110, x=460)
bPrev.place(y=h - 110, x=590)
bNext.place(y=h - 110, x=670)

bShut.place(y=h - 60, x=0)
bHome.place(y=h - 60, x=120)
bClea.place(y=h - 60, x=520)
bPrin.place(y=h - 60, x=670)

time()
readData()
root.after(1000, updateDat)
root.mainloop()
