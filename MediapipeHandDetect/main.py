import PySimpleGUI as sg
import cv2
import mediapipe as mp
from time import sleep
import serial
import pywt

# outSerial = serial.Serial(
#     "COM3",
#     115200,
#     timeout=0.05
# )

first_column = [[sg.Image(filename="", key="-IMAGE0-", size=(400, 400))],
                [sg.Button("Capture 0")],
                [sg.Button("Mulai")]]

second_column = [[sg.Image(filename="", key="-IMAGE1-", size=(400, 400))],
                 [sg.Button("Capture 1")],
                 [sg.Button("Selesai")]]

layout = [[sg.Column(first_column), sg.VSeparator(), sg.Column(second_column)]]

window = sg.Window("Smart Lock Door", layout)

code = 10

cam0 = cv2.VideoCapture(0)
# cam1 = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def main():
    while True:
        event, values = window.read(timeout=20)
        if event == "Selesai" or event == sg.WIN_CLOSED:
            break
        # if event == "Capture 0":
        #     outSerial.write(str(codeS).encode())

        ret, img0 = cam0.read()

        imgRGB = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                h, w, c = img0.shape

                ujungJempol = handLms.landmark[4]
                ujungTelunjuk = handLms.landmark[8]
                ujungTengah = handLms.landmark[12]
                ujungManis = handLms.landmark[16]
                ujungkelingking = handLms.landmark[20]

                Jempol = handLms.landmark[3]
                Telunjuk = handLms.landmark[7]
                Tengah = handLms.landmark[11]
                Manis = handLms.landmark[15]
                Kelingking = handLms.landmark[19]

                x4, y4 = int(ujungJempol.x * w), int(ujungJempol.y * h)
                x8, y8 = int(ujungTelunjuk.x * w), int(ujungTelunjuk.y * h)
                x12, y12 = int(ujungTengah.x * w), int(ujungTengah.y * h)
                x16, y16 = int(ujungManis.x * w), int(ujungManis.y * h)
                x20, y20 = int(ujungkelingking.x * w), int(ujungkelingking.y * h)

                x3, y3 = int(Jempol.x * w), int(Jempol.y * h)
                x7, y7 = int(Telunjuk.x * w), int(Telunjuk.y * h)
                x11, y11 = int(Tengah.x * w), int(Tengah.y * h)
                x15, y15 = int(Manis.x * w), int(Manis.y * h)
                x19, y19 = int(Kelingking.x * w), int(Kelingking.y * h)

                if x4 > x3 and y8 < y7 and y12 < y11 and y16 < y15 and y20 < y19:
                    codeS = 5
                elif x4 < x3 and y8 < y7 and y12 < y11 and y16 < y15 and y20 < y19:
                    codeS = 4
                elif x4 > x3 and y8 < y7 and y12 < y11 and y16 > y15 and y20 > y19:
                    codeS = 3
                elif x4 < x3 and y8 < y7 and y12 < y11 and y16 > y15 and y20 > y19:
                    codeS = 2
                elif x4 < x3 and y8 < y7 and y12 > y11 and y16 > y15 and y20 > y19:
                    codeS = 1
                elif x4 < x3 and y8 < y7 and y12 < y11 and y16 < y15 and y20 > y19:
                    codeS = 6
                elif x4 < x3 and y8 < y7 and y12 < y11 and y16 > y15 and y20 < y19:
                    codeS = 7
                elif x4 < x3 and y8 < y7 and y12 > y11 and y16 < y15 and y20 < y19:
                    codeS = 8
                elif x4 < x3 and y8 > y7 and y12 < y11 and y16 < y15 and y20 < y19:
                    codeS = 9
                else:
                    codeS = 0

                mpDraw.draw_landmarks(img0, handLms, mpHands.HAND_CONNECTIONS)
                print(codeS)

        img0 = cv2.flip(img0, 1)
        imgbytes0 = cv2.imencode(".png", img0)[1].tobytes()
        window["-IMAGE0-"].update(data=imgbytes0)
        sleep(0.1)

        # ret, img1 = cam1.read()
        # imgbytes1 = cv2.imencode(".png", img1)[1].tobytes()
        # window["-IMAGE1-"].update(data=imgbytes1)

    window.close()


main()
