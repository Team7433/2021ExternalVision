import cv2
import cv2.aruco as aruco
import numpy as np
import os
import time

print("2022 FRC 7433 arUco configuration module. Follow instructions on screen. Written by Ali Ashrafy, 2022")

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1.5
color = (255, 0, 0)
thickness = 2


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

def findDistConstant(tr, br, bl, tl, dist=30):
    rightSide = tr[1] - br[1]
    leftSide = tl[1] - bl[1]

    pix = (rightSide + leftSide) / 2
    print(f"Multiply this {pix} by the constant to check how accurate the results are.")

    return pix * dist







while True:
    success, img = cap.read()
    tr, br, bl, tl = findArucoMarkers(img)

    #print(tr, br, bl,tl)
    if tl == None:
        cv2.putText(img, f"Please place the ArUco module exactly 30 cm away from the camera, ", (30, 70), font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(img, f"with it being directly in the center of the field of view.", (30, 150), font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        cv2.putText(img, f"Hold it for 5s, then end program, and check the console for the constant.", (30, 150), font, fontScale, color, thickness, cv2.LINE_AA)
        print(f"Distance constant for this camera is: {findDistConstant(tr,br,bl,tl)}")
    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()