# import cv2
# import numpy as np
# import autopy
# import time
# from HandTrackingModule import handDetector

# print("PROGRAM STARTED")

# wCam, hCam = 640, 480
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(3, wCam)
# cap.set(4, hCam)

# if not cap.isOpened():
#     print("Camera failed to open")
#     exit()

# detector = handDetector(maxHands=1)

# wScr, hScr = autopy.screen.size()

# smoothening = 5
# plocX, plocY = 0, 0
# clocX, clocY = 0, 0
# pTime = 0

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     img = detector.findHands(img)
#     lmList = detector.findPosition(img)

#     if len(lmList) != 0:
#         x1, y1 = lmList[8][1], lmList[8][2]

#         x3 = np.interp(x1, (0, wCam), (0, wScr))
#         y3 = np.interp(y1, (0, hCam), (0, hScr))

#         clocX = plocX + (x3 - plocX) / smoothening
#         clocY = plocY + (y3 - plocY) / smoothening

#         autopy.mouse.move(wScr - clocX, clocY)

#         plocX, plocY = clocX, clocY

#     cTime = time.time()
#     fps = 1 / (cTime - pTime) if pTime != 0 else 0
#     pTime = cTime

#     cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
#                 cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

#     cv2.imshow("AI Virtual Mouse", img)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# print("PROGRAM ENDED")
import cv2
import numpy as np
import autopy
import time
import math
from HandTrackingModule import handDetector

print("PROGRAM STARTED")

# ---------------- SETTINGS ----------------
wCam, hCam = 640, 480
smoothening = 5
clickThreshold = 40

# ------------------------------------------

# Distance function
def findDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

# Webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

if not cap.isOpened():
    print("Camera failed to open")
    exit()

# Hand detector
detector = handDetector(maxHands=1)

# Screen size
wScr, hScr = autopy.screen.size()

# Smooth cursor variables
plocX, plocY = 0, 0
clocX, clocY = 0, 0

pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # Index finger tip
        x1, y1 = lmList[8][1], lmList[8][2]

        # Thumb tip
        x2, y2 = lmList[4][1], lmList[4][2]

        # ---- CURSOR MOVE ----
        x3 = np.interp(x1, (0, wCam), (0, wScr))
        y3 = np.interp(y1, (0, hCam), (0, hScr))

        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        autopy.mouse.move(wScr - clocX, clocY)

        plocX, plocY = clocX, clocY

        # ---- CLICK LOGIC ----
        distance = findDistance((x1, y1), (x2, y2))

        if distance < clickThreshold:
            autopy.mouse.click()
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            time.sleep(0.25)  # prevents multi-click spam

    # FPS Display
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("AI Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("PROGRAM ENDED")
