from csv import reader

datasetcsv = 'dataset.csv'
datasettxt = 'dataset.txt'

datatype = ['String', 'int', 'float', 'float', 'float', 'String']

numrow      = 20
writestring = ''

for index in range(6):
    with open(datasetcsv, 'r') as r:
        csv_reader = reader(r)
        with open(datasettxt, 'a') as w:
            i = 0
            if datatype[index] == 'String':
                for row in csv_reader:
                    if i == 0:
                        writestring = datatype[index] + ' ' + row[index] + '[' + str(numrow) + '] = {"'
                        w.write(writestring)
                    elif i == numrow -1:
                        writestring = row[index] + '"};'
                        w.write(writestring)
                        break
                    else:
                        writestring = row[index] + '","'
                        w.write(writestring)
                    i += 1
                w.writelines('\n')
            else:
                for row in csv_reader:
                    if i == 0:
                        writestring = datatype[index] + ' ' + row[index] + '[' + str(numrow) + '] = {'
                        w.write(writestring)
                    elif i == numrow - 1:
                        writestring = row[index] + '};'
                        w.write(writestring)
                        break
                    else:
                        writestring = row[index] + ','
                        w.write(writestring)

                    i += 1
                w.writelines('\n')
        w.close()
    r.close()
