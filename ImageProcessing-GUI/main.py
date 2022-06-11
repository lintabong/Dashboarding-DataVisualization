import os
import time
import cv2
import numpy
import tkinter
import pandas
import threading
import pywt
import pywt.data
from numpy.linalg   import norm
from PIL            import Image, ImageTk
from collections    import Counter
from scipy          import fft
from time           import sleep

root = tkinter.Tk()
root.option_add('*Font', 30)
root.resizable(False, False)
root.geometry("900x500")
cam = cv2.VideoCapture(0)

# address dataset
dirName = os.path.dirname(str(os.path.abspath(__file__)))
jj = os.path.join(dirName, 'database')
nameDB = os.listdir(jj)
# end

result = []

# format camera
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 6
font_color = (255, 255, 0)
font_thickness = 8

x = 420
y = 200
# end


def L2Norm(h1, h2):
    distance = 0
    for o in range(len(h1)):
        distance += numpy.square(h1[o] - h2[o])

    return numpy.sqrt(distance)


def start_predict():
    u = 0
    while u < 3:
        u += 1
        for i in range(0, 30):
            sleep(0.01)
            _, img = cam.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img, 1)

            if i <= 10:
                cv2.putText(img, str(3), (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
            elif 11 <= i <= 20:
                cv2.putText(img, str(2), (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
            elif 21 <= i <= 26:
                cv2.putText(img, str(1), (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
            else:
                cv2.putText(img, 'Take', (20, 400), font, font_size, font_color, font_thickness, cv2.LINE_AA)


            scale_percent = 70
            width       = int(img.shape[1] * scale_percent / 100)
            height      = int(img.shape[0] * scale_percent / 100)
            dsize       = (width, height)

            img         = cv2.resize(img, dsize)
            img         = Image.fromarray(img)
            imgtk       = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            root.update()

        _, img = cam.read()
        cv2.imwrite('result.jpg', cv2.flip(img, 1))

        scale_percent       = 25
        width               = int(img.shape[1] * scale_percent / 100)
        height              = int(img.shape[0] * scale_percent / 100)
        dsize               = (width, height)
        image               = cv2.resize(img, dsize)
        image               = cv2.flip(image, 1)

        original            = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        coeffs2             = pywt.dwt2(original, 'bior1.3')
        LL, (LH, HL, HH)    = coeffs2

        # Image original
        img                 = Image.fromarray(original)
        imgtk               = ImageTk.PhotoImage(image=img)
        label_RGB.imgtk     = imgtk
        label_RGB.configure(image=imgtk)

        # Image Horizontal
        img                 = Image.fromarray(cv2.resize(LH, (160, 120)))
        imgtk               = ImageTk.PhotoImage(image=img)
        label_biner.imgtk   = imgtk
        label_biner.configure(image=imgtk)

        # Image Gray
        img                 = Image.fromarray(cv2.resize(HL, (160, 120)))
        imgtk               = ImageTk.PhotoImage(image=img)
        label_gray.imgtk    = imgtk
        label_gray.configure(image=imgtk)

        # Image Crop
        img                 = Image.fromarray(cv2.resize(HH, (160, 120)))
        imgtk               = ImageTk.PhotoImage(image=img)
        label_crop.imgtk    = imgtk
        label_crop.configure(image=imgtk)

        threading.Thread(target=exec_predic).start()
        time.sleep(2)


def exec_predic():
    global result

    # RH1 = Counter(cv2.imread('result.jpg').flatten())
    # H1 = []
    #
    # for o in range(256):
    #     if o in RH1.keys():
    #         H1.append(RH1[o])
    #     else:
    #         H1.append(0)
    #
    # dctH1 = fft.dct(H1)

    target = cv2.imread('result.jpg')
    img = numpy.ones([target.shape[0], target.shape[1], 1], dtype="uint8")

    for a in range(img.shape[0]):
        for b in range(img.shape[1]):
            img[a][b] = (int(target[a][b][0]) + int(target[a][b][1]) + int(target[a][b][2]))/3

    morton_target = []
    for s in range(int(img.shape[0]/2), img.shape[0] - 2, 2):
        for d in range(int(img.shape[1]/2), img.shape[1] - 2, 2):
            for a in range(s, 2 + s):
                for b in range(d, 2 + d):
                    morton_target.append(img[a][b][0])

    data = {'name': [], 'val': []}

    for i in range(len(nameDB)):
        cosine = 0
        for r, d, f in os.walk(os.path.join(jj, nameDB[i])):
            for o in range(len(f)):
                # RH2 = Counter(cv2.imread(os.path.join('database', nameDB[i], f[o])).flatten())
                # H2 = []
                # for p in range(256):
                #     if p in RH2.keys():
                #         H2.append(RH2[p])
                #     else:
                #         H2.append(0)
                #
                # dctH2 = fft.dct(H2)
                # mean_distance = mean_distance + L2Norm(dctH1, dctH2)
                db_img = cv2.imread(os.path.join('database', nameDB[i], f[o]))
                img = numpy.ones([db_img.shape[0], db_img.shape[1], 1], dtype="uint8")

                for a in range(img.shape[0]):
                    for b in range(img.shape[1]):
                        img[a][b] = (int(target[a][b][0]) + int(target[a][b][1]) + int(target[a][b][2])) / 3

                morton_db = []
                for s in range(int(img.shape[0]/2), img.shape[0] - 2, 2):
                    for d in range(int(img.shape[1]/2), img.shape[1] - 2, 2):
                        for a in range(s, 2 + s):
                            for b in range(d, 2 + d):
                                morton_db.append(img[a][b][0])

                cosine = cosine + numpy.dot(morton_db, morton_target) / (norm(morton_db) * norm(morton_target))

            cosine = cosine / len(f)

        data['name'].append(nameDB[i])
        data['val'].append(cosine)

    df = pandas.DataFrame(data)
    df.sort_values(by=['val'], inplace=True, ascending=True)
    print(df)
    print(df.iat[0, 0])
    result.append(df.iat[0, 0])


def print_result():
    global result
    if len(result) == 3:
        print(result)
        inValue.delete(0, tkinter.END)
        inValue.insert(0, str(result[0]) + ', ' + str(result[1]) + ', ' + str(result[2]))

        result = []
        root.after(2000, reset_frames)

    root.after(10, print_result)


def reset_frames():
    img                 = cv2.imread('result.jpg')
    scale_percent       = 25
    width               = int(img.shape[1] * scale_percent / 100)
    height              = int(img.shape[0] * scale_percent / 100)
    dsize               = (width, height)
    img                 = cv2.resize(img, dsize)

    cv2image            = 255*numpy.ones(shape=[img.shape[0], img.shape[1], 3], dtype=numpy.uint8)
    img                 = Image.fromarray(cv2image)
    imgtk               = ImageTk.PhotoImage(image=img)
    label_crop.imgtk    = imgtk

    label_biner         .configure(image=imgtk)
    label_RGB           .configure(image=imgtk)
    label_crop          .configure(image=imgtk)
    label_gray          .configure(image=imgtk)


label       = tkinter.Label(root)
label_RGB   = tkinter.Label(root)
label_gray  = tkinter.Label(root)
label_biner = tkinter.Label(root)
label_crop  = tkinter.Label(root)

butStart = tkinter.Button(root, text="Start", width=12, height=2, command=start_predict)

inValue = tkinter.Entry(root, width=20)

label.place(x=10, y=10)
label_RGB.place(x=500, y=10)
label_biner.place(x=680, y=10)
label_gray.place(x=500, y=150)
label_crop.place(x=680, y=150)

butStart.place(x=10, y=400)
inValue.place(x=500, y=300)

print_result()
reset_frames()
root.mainloop()
