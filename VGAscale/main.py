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
