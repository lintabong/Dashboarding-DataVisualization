mytext = input("text: ")
numrow = input("num : ")

numrow = int(numrow)
cuttext = ""
print("text  : ", mytext)

rowprint = int(len(mytext) / numrow)
divider = 0

if len(mytext) >= numrow:
    for u in range(rowprint + 1):
        divider = divider + numrow

        if divider <= rowprint * numrow:
            for i in range(divider - numrow, divider):
                cuttext = cuttext + mytext[i]
        else:
            for i in range(divider - numrow, len(mytext)):
                cuttext = cuttext + mytext[i]
        print("line " + str(u + 1) + ":", cuttext)
        cuttext = ""
