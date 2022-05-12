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


current_dir = os.getcwd()
print(current_dir)
image = cv2.imread("grid1red.png")
side_count = 11 # num squares on a single side of the grid
widthImg = heightImg = side_count * 50
# converts to monochrome
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
    c += 1

# warps perspective to ensure the gridlines are straight as possible
if biggest.size != 0:
    biggest = reorder(biggest)
    cv2.drawContours(image, biggest, -1, (0, 0, 255), 10)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warpedImgColor = cv2.warpPerspective(image, matrix, (widthImg, heightImg))
    warpedImgBW = cv2.cvtColor(warpedImgColor, cv2.COLOR_BGR2GRAY)

# apply the same blur to the new image
blur = cv2.GaussianBlur(warpedImgBW, (5,5), 0)
thresh = cv2.adaptiveThreshold(warpedImgBW, 255, 1, 1, 13, 4)
grid = np.zeros((side_count, side_count), dtype=int)

invert = 255 - thresh
contours2 = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2 = contours2[0] if len(contours2) == 2 else contours2[1]
(contours2, _) = contours.sort_contours(contours2, method = "top-to-bottom")
print(len(contours2))
grid_rows = []
row = []
total = 0
for (i, c) in enumerate(contours2, 1):
    area = cv2.contourArea(c)
    if area > 50:
        row.append(c)
        if i % side_count == 0:
            (contours3, _) = contours.sort_contours(row, method="left-to-right")
            grid_rows.append(contours3)
            row = []

for i, row in enumerate(grid_rows):
    for i2, c in enumerate(row):
        pass

for row in grid_rows:
    for c in row:
        mask = np.zeros(warpedImgColor.shape, dtype=np.uint8)
        cv2.drawContours(mask, [c], -1, (0, 255, 0), 1)
        # cv2.imshow('mask', mask)
        # cv2.waitKey()
        # result = cv2.bitwise_and(warpedImgColor, mask)
        # result[mask==0] = 255
        # cv2.imshow('result', result)
        # cv2.waitKey(15)

print(grid)

cv2.waitKey(0)

cv2.destroyAllWindows()