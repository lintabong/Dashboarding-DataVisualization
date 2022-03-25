from tkinter import *
from escpos import *
from time import strftime
import os

w = 600
h = 400
root = Tk()
root.geometry(str(w) + "x" + str(h))
root.title("Aplikasi Kasir")
root.option_add('*Font', 30)

bgHead = "#afa013"
bgSeco = "#dbcb33"
white  = "#ffffff"

def time():
    time_utc = strftime("%I:%M:%S %p") + "    " + strftime("%a, %b %d, %Y")
    textDate.config(text=time_utc)
    root.after(1000, time)


def printValue():
    getName     = inName.get()
    getPhone    = inPhone.get()
    getAddress  = inAddress.get()
    time_utc    = strftime("%I:%M:%S") + " " + strftime("%a, %b %d, %Y")

    numrow      = 32
    cutAddress  = ""
    rowPrint    = int(len(getAddress) / numrow)
    divider     = 0

    print("--------------------------------")
    print(str(time_utc))
    print(" ")
    print("Pengirim : Lintang")
    print("No. HP   : 082221398970")
    print("================================")
    print(getName, getPhone)

    if len(getAddress) >= numrow:
        for u in range(rowPrint + 1):
            divider = divider + numrow

            if divider <= rowPrint * numrow:
                for i in range(divider - numrow, divider):
                    cutAddress = cutAddress + getAddress[i]

            else:
                for i in range(divider - numrow, len(getAddress)):
                    cutAddress = cutAddress + getAddress[i]

            print(cutAddress)
            cutAddress = ""
    print("--------------------------------")


def clearValue():
    inName      .delete(0, END)
    inPhone     .delete(0, END)
    inAddress   .delete(0, END)
    print("clear succes")


frame0 = Frame(root, bg=bgHead, width=w, height=35)
frame1 = Frame(root, bg=bgSeco, width=w, height=h - 100)

textDate    = Label(frame0, bg=bgHead, fg=white)
textResi    = Label(frame1, bg=bgSeco, fg=white, text="Resi")
textName    = Label(frame1, bg=bgSeco, fg=white, text="Nama Pembeli")
textPhone   = Label(frame1, bg=bgSeco, fg=white, text="Nomer Telepon")
textAddress = Label(frame1, bg=bgSeco, fg=white, text="Alamat:")
inResi      = Entry(frame1, width=20)
inName      = Entry(frame1, width=20)
inPhone     = Entry(frame1, width=20)
inAddress   = Entry(frame1, width=20)
butPrint    = Button(frame1, width=10, height=2, text="Cetak", command=printValue)
butClear    = Button(frame1, width=10, height=2, text="clear", command=clearValue)

butMenuResi     = Button(root, width=10, height=2, text="Cetak Resi")
butMenuProduct  = Button(root, width=10, height=2, text="Produk")

frame0.place(y=0, x=0)
frame1.place(y=35, x=0)

textDate    .place(y=8  , x=w-250)
textResi    .place(y=20 , x=10)
textName    .place(y=50 , x=10)
textPhone   .place(y=80 , x=10)
textAddress .place(y=110, x=10)
inResi      .place(y=20 , x=140)
inName      .place(y=50 , x=140)
inPhone     .place(y=80 , x=140)
inAddress   .place(y=110, x=140)
butPrint    .place(y=220, x=10)
butClear    .place(y=220, x=140)

butMenuResi     .place(y=345, x=10)
butMenuProduct  .place(y=345, x=120)

time()
root.mainloop()
