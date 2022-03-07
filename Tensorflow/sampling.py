import cv2
from time import sleep
import os

myName = input('name = ')
myName = str(myName)
mypath = os.path.abspath(__file__)
dirName = os.path.dirname(str(mypath))
directories = os.listdir(dirName)

os.mkdir(dirName + '/' + myName)

cam = cv2.VideoCapture(0)
i = 0
while True:
    ret, img = cam.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img, 1)
    cv2.imshow("frame", img)

    i = i + 1
    cv2.imwrite(dirName + '/' + myName + '/' + myName + str(i) + '.jpg', img)
    sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q') or i == 300:
        break

cam.release()
cv2.destroyAllWindows()
