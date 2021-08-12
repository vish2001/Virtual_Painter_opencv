import cv2
import numpy as np
###############################################
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
#Use color picker to get the color.
mycolors = [[101,56,90,154,255,255]] # H-min S-min V-min H-max S-max V-max
# [5,107,0,19,255,255]][0, 76, 153, 39, 255, 255],
colorvalues = [[25, 255, 255]]
mypoints = []  # [x,y,colorId]
################################################

def findcolor(img, mycolors, colorvalues): #Function to detect a particular colour (listed in the mycolors list) from the image
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for colors in mycolors:
        lower = np.array(colors[0:3])
        upper = np.array(colors[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgresult, (x, y), 5, colorvalues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(colors[0]),mask)
    return newPoints


def getContours(img): # Function for contour detection
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, z, w = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # To reduce noise
            cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
            #print(len(approx))
            objcor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(mypoints, colorvalues):
    for point in mypoints:
        cv2.circle(imgresult, (point[0], point[1]), 5, colorvalues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgresult = img.copy()
    newPoints = findcolor(img, mycolors, colorvalues)
    if len(newPoints) != 0:
        for newP in newPoints:
            mypoints.append(newP)
    if len(mypoints) != 0:
        drawOnCanvas(mypoints, colorvalues)
    flipped = cv2.flip(imgresult, 1)
    cv2.imshow("Result", flipped)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
