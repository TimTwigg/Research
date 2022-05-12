import numpy as np
import cv2
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
image = cv2.imread("grid1red.png")
side_count = 11 # num squares on a single side of the grid
widthImg = heightImg = side_count * 50 + 50
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
    c += 1

# warps perspective to ensure the gridlines are straight as possible
if biggest.size != 0:
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warpedImgColor = cv2.warpPerspective(image, matrix, (widthImg, heightImg))
    warpedImgBW = cv2.cvtColor(warpedImgColor, cv2.COLOR_BGR2GRAY)

def isRed(color):
    if color[0] not in range(0,7):
        return False
    if color[1] not in range(0, 100):
        return False
    if color[2] not in range(100, 256):
        return False
    return True

grid = np.zeros((side_count, side_count), dtype=int)

for x in range (1, side_count + 1):
    for y in range (1, side_count + 1):
        cv2.circle(warpedImgColor, (50 * x, 50 * y), 2, (0, 255, 0))
        if isRed(warpedImgColor[x * 50, y * 50]):
            grid[x - 1, y - 1] = 1

        

cv2.imshow("image", warpedImgColor)
print(grid)

cv2.waitKey(0)
