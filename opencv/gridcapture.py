# https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv

import cv2
import gridReaderFinal as gr

def screenshot():
    '''Returns the grid from the captured image.
    If no image was captured, returns empty string.
    NOTE: Save path changes depending on which directory makes the call to this module.'''
    return_grid = ""
    cam = cv2.VideoCapture(2) # THIS LINE WILL CHANGE TO FIT DESIRED CAMERA

    cv2.namedWindow("test")

    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
    else:
        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
                
            elif k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_0.png" # Same image gets overwritten with every capture. No multiple images
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                res = gr.GridReader(img_name, 15)
                return_grid = res.readGrid()
                print(return_grid)
            
            if cv2.getWindowProperty("test", cv2.WND_PROP_VISIBLE) < 1:
                print("User pressed X on the window")
                break

    cam.release()
    cv2.destroyAllWindows()
    return return_grid

if __name__ == "__main__":
    screenshot()