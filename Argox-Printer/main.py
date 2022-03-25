import serial
from time import sleep

ser = serial.Serial(
    port="COM31",
    baudrate=9600,
    timeout=0.05
)

serP = serial.Serial(
    port="COM7",
    baudrate=9600,
    timeout=0.05
)


while True:
    data = ser.readline()
    strData = str(data)
    strData = strData.replace('\\r\\n', "")
    strData = strData.replace('GS', "")
    strData = strData.replace('G', "")
    strData = strData.replace('\'', "")
    strData = strData.replace('+', "")
    strData = strData.replace('b', "")
    strData = strData.replace(' ', "")


    # print(data)
    if strData != '':
        fltData = float(strData)
        print(strData, fltData)

        unit = 'A290,290,0,4,2,2,N,"g"\r\n'
        datePrint = 'A30,60,0,4,1,1,N,TDyy-me-dd\r\n'
        timePrint = 'A250,60,0,4,1,1,N,TTh:m:s\r\n'
        mat = 'A20,120,0,4,1,1,N,"MATERIAL : VIT 07 15 SCI"\r\n'
        label = 'A70,0,0,4,2,2,N,"INDOKUAT"\r\n'
        SKU  = 'A20,150,0,4,1,1,N,"SKU  : CHOCHO: 15 TON"\r\n'
        OPR  = 'A20,180,0,4,1,1,N,"OPR  : KTB/TSM/JRT/WHY"\r\n'
        LINE = 'A20,210,0,4,1,1,N,"LINE : SCI"\r\n'
        LOT  = 'A20,240,0,4,1,1,N,"LOT  : 210801216"\r\n'

        serP.write(label.encode())
        serP.write(mat.encode())
        serP.write(SKU.encode())
        serP.write(OPR.encode())
        serP.write(LINE.encode())
        serP.write(LOT.encode())

        if fltData >= 1000.00:
            value = strData
            gabung = 'A50,290,0,4,2,2,N,"' + value + '"\r\n'

        else:
            value = strData
            gabung = 'A80,290,0,4,2,2,N,"' + value + '"\r\n'

        serP.write(unit.encode())
        serP.write(timePrint.encode())
        serP.write(datePrint.encode())
        serP.write(gabung.encode())
        serP.write('P1\r\n'.encode())
    sleep(1)
