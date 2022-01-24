import cv2
import cv2.aruco as aruco
import time
import math
import constants


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0,255,255)
thickness = 2





def findArucoMarkers(img, markerSize = 6, totalMarkers=250):
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

        cv2.line(img, topLeft, topRight, (0,255,0), 6)
        cv2.line(img, topRight, bottomRight, (0,255,0), 6)
        cv2.line(img, bottomRight, bottomLeft, (0,255,0), 6)
        cv2.line(img, bottomLeft, topLeft, (0,255,0), 6)



        return topRight, bottomRight, bottomLeft, topLeft
    else:
        return None, None, None, None


def getDiffSides(tr, br, tl, bl):
    if tr == None:
        return None
    else:
        trX, trY = tr
        brX, brY = br
        tlX, tlY = tl
        blX, blY = bl
        rightSideLength = trY - brY
        leftSideLength = tlY - blY

        diffSides  = rightSideLength - leftSideLength

        diffSides = diffSides ** 2
        diffSides = math.sqrt(diffSides)

        return diffSides


def findAngle(tr,br,tl,bl):
    diff = getDiffSides(tr,br,tl,bl)
    distance = findDistance(tr,br,tl,bl)
    j = (constants.kOptimalPixels / diff) / (constants.kOptimalDistance / distance)
    return constants.kOptimalAngle / j


def findDistance(tr,br,tl,bl):
    trX, trY = tr
    brX, brY = br
    tlX, tlY = tl
    blX, blY = bl
    rightSide = trY - brY
    leftSide = tlY - blY
    pix = rightSide + leftSide
    pix /= 2
    return pix


def findCoordinates(distance, angle, original_position=(2,0)):
    phi = distance * math.cos(angle)
    b = (distance ** 2) + (phi ** 2)
    b = math.sqrt(b)
    i, j = original_position
    i += b
    j += phi

    return b,phi


cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()
    tr, br, bl, tl = findArucoMarkers(img)

    if tr == None:
        #print(None)
        pass
    else:
        pix = findDistance(tr,br,tl,bl)
        print(getDiffSides(tr, br, tl, bl))
        print(findAngle(tr, br, tl, bl))
        coords = findCoordinates(findDistance(tr,br,tl,bl), findAngle(tr,br,tl,bl))
        angle = findAngle(tr,br,tl,bl)

        #print(pix)

        dist = constants.kDistanceCalculationConstant/pix
        cv2.putText(img, f"Distance: {dist}", tr, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(img, f"Coords: {coords}", tl, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(img, f"Angle: {angle}", br, font, fontScale, color, thickness, cv2.LINE_AA)
        #print(dist)




    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()