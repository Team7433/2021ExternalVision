import cv2
import cv2.aruco as aruco

const = 4900
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

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()
    tr, br, bl, tl = findArucoMarkers(img)
    if tr == None:
        print(None)
    else:
        trX, trY = tr
        brX, brY = br
        pix = brY-trY

        dist = const/pix
        image = cv2.putText(img, f"Distance: {dist}", tl, font, fontScale, color, thickness, cv2.LINE_AA)
        print(dist)




    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()