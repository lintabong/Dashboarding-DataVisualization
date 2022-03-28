from tkinter import *
from escpos import *
from time import strftime
import os
import pyrebase
import time

firebaseConfig = {
    'apiKey': "*******YcooVCdT6yk75qXsviyqBU",
    'authDomain': "*******-20f3a.firebaseapp.com",
    'databaseURL': "https://*******-20f3a-default-rtdb.firebaseio.com",
    'projectId': "*******-20f3a",
    'storageBucket': "*******-20f3a.appspot.com",
    'messagingSenderId': "*******2340922",
    'appId': "*******28e4c503",
    'measurementId': "*******8KWQF0"
}

firebase    = pyrebase.initialize_app(firebaseConfig)
storage     = firebase.storage()
db          = firebase.database()

w = 600
h = 400
root = Tk()
root.geometry(str(w) + "x" + str(h))
root.title("Aplikasi Kasir")
root.option_add('*Font', 30)

bgHead = "#afa013"
bgSeco = "#dbcb33"
white = "#ffffff"

try:
    os.system("sudo chmod 666")
except:
    pass


def dateCounter():
    time_utc = strftime("%I:%M:%S %p") + "    " + strftime("%a, %b %d, %Y")
    textDate.config(text=time_utc)
    root.after(1000, dateCounter)


def printValue():
    getName = inName.get()
    getPhone = inPhone.get()
    getAddress = inAddress.get()
    time_utc = strftime("%I:%M:%S") + " " + strftime("%a, %b %d, %Y")

    numrow = 32
    cutAddress = ""
    rowPrint = int(len(getAddress) / numrow)
    divider = 0

    time.sleep(0.1)
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
    inName.delete(0, END)
    inPhone.delete(0, END)
    inAddress.delete(0, END)
    print("clear success")


def changePrint():
    frameInput.place_forget()
    framePrint.place(y=35 , x=0)


def changeInputProduct():
    framePrint.place_forget()
    frameInput.place(y=35 , x=0)


category = db.child("category").get().val()
listCategory    = []
buffCategory    = ""
listProduct     = ["none"]
for k, v in category.items():
    listCategory.append(k)

def getOptCategory(selection):
    global k, v
    global buffCategory
    buffCategory = selection
    product = db.child('category').child(selection).get().val()
    listProduct.clear()
    for k, v in product.items():
        print(v['name'])
        listProduct.append(v['name'])

    OptionMenu(frameInput, chosenProduct, *listProduct, command=getOptProduct).place(y=60, x=100)


def getOptProduct(selection):
    global k, v
    global buffCategory
    inProductName   .delete(0, END)
    inProductPrize  .delete(0, END)
    inProductSKU    .delete(0, END)
    inProductStock  .delete(0, END)

    product = db.child('category').child(buffCategory).get().val()
    for k, v in product.items():
        if v['name'] == selection:
            inProductName   .insert(0, v['name'])
            inProductPrize  .insert(0, v['prize'])
            inProductSKU    .insert(0, v['sku'])
            inProductStock  .insert(0, v['stock'])

frameDate           = Frame(root, bg=bgHead, width=w, height=100)
frameInput          = Frame(root, bg=bgSeco, width=w, height=h - 100)
framePrint          = Frame(root, bg=bgSeco, width=w, height=h - 100)

butMenuResi         = Button(root, width=10, height=2, text="Cetak Resi", command=changePrint)
butMenuProduct      = Button(root, width=10, height=2, text="Produk", command=changeInputProduct)

textDate            = Label(root, bg=bgHead, fg=white)

textResi            = Label(framePrint, bg=bgSeco, fg=white, text="Resi")
textName            = Label(framePrint, bg=bgSeco, fg=white, text="Nama Pembeli")
textPhone           = Label(framePrint, bg=bgSeco, fg=white, text="Nomer Telepon")
textAddress         = Label(framePrint, bg=bgSeco, fg=white, text="Alamat:")
inResi              = Entry(framePrint, width=20)
inName              = Entry(framePrint, width=20)
inPhone             = Entry(framePrint, width=20)
inAddress           = Entry(framePrint, width=20)
butPrint            = Button(framePrint, width=10, height=2, text="Cetak", command=printValue)
butClear            = Button(framePrint, width=10, height=2, text="clear", command=clearValue)

textCategory        = Label(frameInput, bg=bgSeco, fg=white, text="Kategori")
textProduct         = Label(frameInput, bg=bgSeco, fg=white, text="Produk")
chosenCategory      = StringVar()
chosenProduct       = StringVar()
optCategory         = OptionMenu(frameInput, chosenCategory, *listCategory, command=getOptCategory)
optProduct          = OptionMenu(frameInput, chosenProduct, *listProduct)
textProductName     = Label(frameInput, bg=bgSeco, fg=white, text="Nama Produk")
textProductPrize    = Label(frameInput, bg=bgSeco, fg=white, text="Harga")
textProductSKU      = Label(frameInput, bg=bgSeco, fg=white, text="SKU")
textProductStock    = Label(frameInput, bg=bgSeco, fg=white, text="Stock")
inProductName       = Entry(frameInput, width=20)
inProductPrize      = Entry(frameInput, width=20)
inProductSKU        = Entry(frameInput, width=20)
inProductStock      = Entry(frameInput, width=20)
line0               = Frame(frameInput, bg=bgHead, width=3, height=270)

# ==================PLACEMENT======================= #

frameDate           .place(y=0  , x=0)
frameInput          .place(y=35 , x=0)
framePrint          .place(y=35 , x=0)
butMenuResi         .place(y=345, x=10)
butMenuProduct      .place(y=345, x=120)

textDate    .place(y=8  , x=w - 250)
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

textCategory.place(y=20 , x=10)
textProduct .place(y=60 , x=10)
optCategory .place(y=20 , x=100)
optProduct  .place(y=60 , x=100)

textProductName     .place(y=120 , x=10)
textProductPrize    .place(y=150 , x=10)
textProductSKU      .place(y=180 , x=10)
textProductStock    .place(y=210 , x=10)
inProductName       .place(y=120 , x=130)
inProductPrize      .place(y=150 , x=130)
inProductSKU        .place(y=180 , x=130)
inProductStock      .place(y=210 , x=130)
line0               .place(y=15  , x=330)

dateCounter()
root.mainloop()
