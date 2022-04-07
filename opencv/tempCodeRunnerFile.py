y = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# c = 0
# for i in cnts:
#     area = cv2.contourArea(i)
#     if area > 1000/2:
#         cv2.drawContours(warpedImgColor, cnts, c, (0, 0, 0), 2)
#     c += 1
# cv2.imshow("