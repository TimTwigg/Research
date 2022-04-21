import cv2
from imutils import contours
import numpy as np
import os

# code generously donated from (i stole it from) https://stackoverflow.com/questions/36508001/determining-if-a-color-is-within-a-contour-opencv

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

count = 0
max_size = 0
matrix = []
new_contours = []
grid_contour = 0
grid_contour_row = None
grid_contour_column = None
for each in enumerate(cnts):

    # used to find midpoints
    M = cv2.moments(cnts[count])
    row = int(M['m10']/M['m00'])
    column = int(M['m01']/M['m00'])

    size = cv2.contourArea(cnts[count])
    if(size > max_size):
        new_contours.append(cnts[grid_contour])
        # mark each cell for testing
        if (grid_contour_row != None and grid_contour_column != None):
            cv2.putText(image, "0", \
                    (grid_contour_row, grid_contour_column), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        grid_contour = count
        grid_contour_row = row
        grid_contour_column = column
    else:
        new_contours.append(cnts[count])
    count += 1

# draw lines around contours
cv2.drawContours(image, new_contours, -1, (0, 255, 0))

#apr
