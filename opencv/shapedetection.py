import cv2
import numpy as np


def getContours(img):
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        cv2.drawContours(doodoo, cnt, -1, (255, 0, 0), 3)


path = "shapes.png"
img = cv2.imread(path)
doodoo = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)

getContours(imgCanny)
cv2.imshow("yamama", doodoo)
cv2.imshow("yamama2", imgGray)
cv2.imshow("yamama3", imgBlur)
cv2.imshow("yamama4", imgCanny)

cv2.waitKey(0)