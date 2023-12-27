import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the webcam and set its dimensions
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize hand detector with a confidence threshold
detector = HandDetector(detectionCon=0.8)

# Set color for the rectangles
colorR = (255, 0, 255)

# Function to calculate the distance between two points
def calculateDistance(x1, y1, x2, y2):
    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

# Class representing a draggable rectangle
class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy, _ = self.posCenter
        w, h = self.size

        # Check if the cursor is inside the rectangle
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            # Update the position of the rectangle to the cursor position
            self.posCenter = cursor

# Create a list of draggable rectangles
rectList = [DragRect([x * 250 + 150, 150, 0]) for x in range(5)]

# Main loop for capturing and processing frames
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not success:
        print("Failed to capture frame. Exiting...")
        break

    # Detect hands in the frame
    hands, img = detector.findHands(img)

    if hands and len(hands) > 0:
        lmList = hands[0]["lmList"]
        if lmList:
            # Iterate through each draggable rectangle
            for rect in rectList:
                # Calculate the distance between the index finger and the center of the rectangle
                distance = calculateDistance(lmList[8][0], lmList[8][1], rect.posCenter[0], rect.posCenter[1])
                print(distance)

                # If the distance is less than 30 pixels, update the rectangle's position to the cursor
                if distance < 30:
                    cursor = lmList[8]
                    rect.update(cursor)

    # Draw the rectangles on the frame
    for rect in rectList:
        cx, cy, _ = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (int(cx - w // 2), int(cy - h // 2)), (int(cx + w // 2), int(cy + h // 2)), colorR, cv2.FILLED)

    # Display the frame
    cv2.imshow("image", img)

    # Break the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cv2.destroyAllWindows()
cap.release()
