import cv2
import numpy as np
import time

capture = cv2.VideoCapture("./video.mp4")

time.sleep(1)
count = 0
background = 0

#capture background in range of 60
for i in range(60):
    return_value, background = capture.read()
    if return_value == False:
        continue

#flip the frame
background = np.flip(background, axis = 1)

#convert default resolution from float to integer
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))

#define codec
video = cv2.VideoWriter('invisibility_cloak.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width, frame_height))

#read from video
while (capture.isOpened()):
    return_value, img = capture.read()
    if not return_value:
        break
    count += 1
    img = np.flip(img, axis = 1)

    #convert BGR to HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #mask1 range(hsv image, lower limit, upper limit) 
    mask1 = cv2.inRange(img_hsv, np.array([100, 40, 40]), np.array([100, 255, 255]))

    #mask2 range(hsv image, lower limit, upper limit)
    mask2 = cv2.inRange(img_hsv, np.array([155, 40, 40]), np.array([180, 255, 255]))

    mask1 = mask1 + mask2

    #refine mask
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    #final output
    output1 = cv2.bitwise_and(background, background, mask = mask1)
    output2 = cv2.bitwise_and(img, img, mask=mask2)
    output = cv2.addWeighted(output1, 1, output2, 1, 0)

    #video
    video.write(output)

    #display
    cv2.imshow("Invisibility Cloak", output)

    key = cv2.waitKey(10)
    if key == 27:
        break

#release video capture and video write objects
capture.release()
video.release()

cv2.destroyAllWindows()
