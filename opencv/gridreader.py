import cv2
from imutils import contours
import numpy as np
import os


def reorder(points):
    points = points.reshape((4, 2))
    npoints = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    npoints[0] = points[np.argmin(add)]
    npoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    npoints[1] = points[np.argmin(diff)]
    npoints[2] = points[np.argmax(diff)]
    return npoints

# imports image
current_dir = os.getcwd()
print(current_dir)
image = cv2.imread(r"C:\Users\vitoc\Documents\Coding Projects\Research\opencv\grid1red.png")
side_count = 11 # num squares on a single side of the grid
widthImg = heightImg = side_count * 50
# converts to monochrome
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blurs image slightly
# blur = cv2.GaussianBlur(gray, (5,5), 0)
# adaptive thresholding                             this digit controls how much gets subtracted
thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 13, 10)

# finds all contours
cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# finds the largest square, the border of the grid
max_area = 0
c = 0
for i in cnts:
    area = cv2.contourArea(i)
    if area > 1000:
        permiter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, .02 * permiter, True)
        if area > max_area and len(approx) == 4: 
            max_area = area
            biggest = i
            #image = cv2.drawContours(image, cnts, c, (0, 255, 0), 3)
    c += 1

# warps perspective to ensure the gridlines are straight as possible
if biggest.size != 0:
    biggest = reorder(biggest)
    # cv2.drawContours(image, biggest, -1, (0, 0, 255), 10)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warpedImgColor = cv2.warpPerspective(image, matrix, (widthImg, heightImg))
    warpedImgBW = cv2.cvtColor(warpedImgColor, cv2.COLOR_BGR2GRAY)

# apply the same blur to the new image
blur = cv2.GaussianBlur(warpedImgBW, (5,5), 0)
thresh = cv2.adaptiveThreshold(warpedImgBW, 255, 1, 1, 13, 4)
cv2.imshow("first thresh", thresh)

# finds all contours again
# cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# c = 0
# for i in cnts:
#     area = cv2.contourArea(i)
#     if area > 1000/2:
#         cv2.drawContours(warpedImgColor, cnts, c, (0, 0, 0), 2)
#     c += 1
# cv2.imshow("warpedcolor", warpedImgColor)

# Red
hsv = cv2.cvtColor(warpedImgColor, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 100, 100])
upper_red = np.array([7, 255, 255])
red = cv2.inRange(hsv, lower_red, upper_red)

# grid = np.zeros((side_count, side_count), dtype=int)
# r = 0
# c = -1
# for i in contours:
#     area = cv2.contourArea(i)
#     if area > 50 and area < max_area:
#         perimiter = cv2.arcLength(i, True)
#         approx = cv2.approxPolyDP(i, .02 * perimiter, True)
#         if len(approx) == 4:
#             c += 1
#             x,y,w,h = cv2.boundingRect(i)
#             current = cv2.rectangle(warpedImgColor, (x,y), (x+w, y+h), (0, 0, 0), 2)
#             print(f'Average color of {r}, {c}: ', cv2.mean(current))
#             cv2.imshow('cut', warpedImgColor[y:y+h, x:x+w])
#             if c % side_count == 0:
#                 r += 1
#                 c = 0


invert = 255 - thresh
cv2.imshow("invert", invert)
contours2 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2 = contours2[0] if len(contours2) == 2 else contours2[1]
(contours2, _) = contours.sort_contours(contours2, method = "top-to-bottom")
grid_rows = []
row = []
for (i, c) in enumerate(contours2, 1):
    area = cv2.contourArea(c)
    if area > 50:
        row.append(c)
        if i % 9 == 0:
            (contours2, _) = contours.sort_contours(row, method="left-to-right")
            grid_rows.append(contours2)
            row = []
for row in grid_rows:
    for c in row:
        mask = np.zeros(warpedImgColor.shape, dtype=np.uint8)
        # cv2.drawContours(mask, [c], -1, (255, 255, 255), 1)
        result = cv2.bitwise_and(warpedImgColor, mask)
        result[mask==0] = 255
        cv2.imshow('result', result)
        cv2.waitKey(20)


            # current = warpedImgColor[y:y+h, x:x+w]
        #     cv2.imshow('cut', warpedImgColor[y:y+h, x:x+w])
        #     print('Average color (BGR): ', 
        #     np.array(cv2.mean(warpedImgColor[y:y+h, x:x+w])).astype(np.uint8))

cv2.waitKey(0)

cv2.destroyAllWindows()