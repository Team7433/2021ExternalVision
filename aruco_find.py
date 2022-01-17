import cv2
import cv2.aruco as aruco
import time
import math


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0,255,255)
thickness = 2
const = 4830




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

def findkProportion(distance=30, do = False, img = None):
    if do == False:
        return distance
    elif do == True:
        for count in range(5, 1):
            time.sleep(1)
            cv2.putText(img, f"{count}", (10,10), font, fontScale, color, thickness, cv2.LINE_AA)


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
cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()
    findkProportion(img=img, do=True)
    tr, br, bl, tl = findArucoMarkers(img)
    print(getDiffSides(tr,br,tl,bl))
    if tr == None:
        #print(None)
        pass
    else:
        trX, trY = tr
        brX, brY = br
        tlX, tlY = tl
        blX, blY = bl
        topleft = trY+tlY
        topleft /= 2
        topRight = brY+blY
        topRight /= 2
        pix = topRight - topleft
        #print(pix)

        dist = const/pix
        image = cv2.putText(img, f"Distance: {dist}", tl, font, fontScale, color, thickness, cv2.LINE_AA)
        #print(dist)




    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()