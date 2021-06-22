import cv2
import cv2.aruco as aruco
import numpy as np
import os
import time
import math

def findArucoMarkers(img, markerSize = 6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')

    arucoDict = aruco.Dictionary_get(key)

    arucoParam = aruco.DetectorParameters_create()

    (corners, ids, rejected) = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)
    if len(corners) > 0:

        ids=ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):

            corners = markerCorner.reshape((4,2))

            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

        cv2.line(img, topLeft, topRight, (0,255,0), 2)
        cv2.line(img, topRight, bottomRight, (0,255,0), 2)
        cv2.line(img, bottomRight, bottomLeft, (0,255,0), 2)
        cv2.line(img, bottomLeft, topLeft, (0,255,0), 2)


        return topRight, bottomRight, bottomLeft, topLeft
    else:
        return None, None, None, None

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()
    tr, br, bl, tl = findArucoMarkers(img)
    print(tr, br, bl, tl)

    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()