import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)


def calculateDistance(x1, y1, x2, y2):
    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy, _ = self.posCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor


rectList = []

for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150, 0]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not success:
        print("Failed to capture frame. Exiting...")
        break

    hands, img = detector.findHands(img)

    if hands and len(hands) > 0:
        lmList = hands[0]["lmList"]
        if lmList:
            for rect in rectList:
                distance = calculateDistance(lmList[8][0], lmList[8][1], rect.posCenter[0], rect.posCenter[1])
                print(distance)

                if distance < 30:
                    cursor = lmList[8]
                    rect.update(cursor)

    for rect in rectList:
        cx, cy, _ = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (int(cx - w // 2), int(cy - h // 2)), (int(cx + w // 2), int(cy + h // 2)), colorR, cv2.FILLED)

    cv2.imshow("image", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()
