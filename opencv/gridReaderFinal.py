import numpy as np
import cv2

class GridReader:
    def __init__(self, image: str, squares_on_side: int):
        '''
        image -- path to theimage
        squares_on_side -- number of squares on a single side of the grid
        '''
        self.__image = cv2.imread(image)
        self.__squares_on_side = squares_on_side # num squares on a single side of the grid
        self.__widthImg = self.__heightImg = self.__squares_on_side * 50 + 50 # size of the image in pixels
        self.__grid = np.zeros((self.__squares_on_side, self.__squares_on_side), dtype=int)
        self.__warped = self.warp(self.threshImage())


    def setImage(self, new_image: "image"):
        '''
        Changes the image the object is reading. 

        new_image -- path to the new image
        '''
        self.__image == new_image

    def setSide(self, new_side_length: int):
        '''
        Changes the number of squares on one side to inputted number. 

        new_side_length -- int for new number of sides
        '''
        self.__squares_on_side = new_side_length


    def reorder(self, points: np.ndarray) -> np.ndarray:
        '''
        Takes an array of points and orders them properly from left -> right, top -> bottom. 
        
        points -- array of points to reorder

        returns: sorted array of points
        '''
        print(points.shape)
        points = points.reshape((4, 2))
        npoints = np.zeros((4, 1, 2), dtype=np.int32)
        add = points.sum(1)
        npoints[0] = points[np.argmin(add)]
        npoints[3] = points[np.argmax(add)]
        diff = np.diff(points, axis=1)
        npoints[1] = points[np.argmin(diff)]
        npoints[2] = points[np.argmax(diff)]
        return npoints

    def threshImage(self) -> "image":
        '''
        Takes a source image and converts it to monochrome, blurs it, and applies adaptive thresholding. 
        It then returns the result of this processing.

        returns: image 
        '''
        # converts to monochrome
        gray = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
        # blurs image slightly
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        # adaptive thresholding                             this digit controls how much gets subtracted
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 13, 10)

        return thresh

    def warp(self, thresh: "image") -> "image":
        '''
        Takes a threshed image as input and warps it to class specified size and returns the warped image.

        thresh -- threshed image of grid

        returns: image (self.widthImg x self.heightImg)
        '''
        # finds all contours
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(thresh, cnts, -1,(255, 255, 255), 3)

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
        cv2.imshow('name of the window', thresh)
        cv2.waitKey(0)
        # warps perspective to ensure the gridlines are straight as possible
        if biggest.size != 0:
            print(f'biggest: {biggest}')
            biggest = self.reorder(biggest)
            pts1 = np.float32(biggest)
            pts2 = np.float32([[0, 0], [self.__widthImg, 0], [0, self.__heightImg], [self.__widthImg, self.__heightImg]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            return cv2.warpPerspective(self.__image, matrix, (self.__widthImg, self.__heightImg))

    def isRed(self, color: list[int]) -> bool:
        '''
        Checks if provided BGR color is red or not, then returns true or false.

        color -- a list of 3 ints representing BGR color

        returns: bool, true if red, false if not
        '''
        if color[0] not in range(0,7):
            return False
        if color[1] not in range(0, 100):
            return False
        if color[2] not in range(100, 256):
            return False
        return True

    def readGrid(self) -> np.ndarray:
        '''
        Reads the grid image. If there are squares containing red, their number in the grid
        is changed to a 1. Returns the grid.

        returns: 2d array, 0 denoting white, 1 denoting red
        '''
        for x in range (1, self.__squares_on_side + 1):
            for y in range (1, self.__squares_on_side + 1):
                cv2.circle(self.__warped, (50 * x, 50 * y), 2, (0, 255, 0))
                if self.isRed(self.__warped[x * 50, y * 50]):
                    self.__grid[x - 1, y - 1] = 1
        return(self.__grid)

if __name__ == '__main__':
    #r = GridReader('grid1red.png', 1y)
    r = GridReader('opencv_frame_0.png', 18)
    
    print(r.readGrid())
