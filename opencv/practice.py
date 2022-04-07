import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while True:
        success, img = cap.read()
        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        """
def empty(x):
    pass

img = cv2.imread("shapes.jpg")

cv2.namedWindow("trackbars")
cv2.resizeWindow("trackbars", 640, 240)
cv2.createTrackbar("HueMin", "trackbars", 0, 179, empty)
cv2.createTrackbar("HueMax", "trackbars", 179, 179, empty)
cv2.createTrackbar("SatMin", "trackbars", 0, 255, empty)
cv2.createTrackbar("SatMax", "trackbars", 255, 255, empty)
cv2.createTrackbar("ValMin", "trackbars", 0, 255, empty)
cv2.createTrackbar("ValMax", "trackbars", 255, 255, empty)

while True:
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HueMin", "trackbars")
    h_max = cv2.getTrackbarPos("HueMax", "trackbars")
    s_min = cv2.getTrackbarPos("SatMin", "trackbars")
    s_max = cv2.getTrackbarPos("SatMax", "trackbars")
    v_min = cv2.getTrackbarPos("ValMin", "trackbars")
    v_max = cv2.getTrackbarPos("ValMax", "trackbars")

    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    kernel = np.ones((5, 5), np.uint8)

    cv2.imshow("img", img)
    cv2.imshow("imghsv", imgHSV)
    cv2.imshow("mask", mask)
    cv2.imshow("and", result)

    cv2.waitKey(1)"""
'''
cap = cv2.VideoCapture(0)
caphsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while True:
        success, img = cap.read()
        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break'''

#imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
#imgCanny = cv2.Canny(img, 150, 200)
#imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
#imgErosion = cv2.erode(imgDilation, kernel, iterations=1)



# cv2.imshow("Your Mother", imgGray)
# cv2.imshow("Your Mother but Blurry", imgBlur)
# cv2.imshow("Your Mother but Canny", imgCanny)
# cv2.imshow("Your Mother but Dilation", imgDilation)
#cv2.imshow("Your Mother but Eroded", imgErosion)
