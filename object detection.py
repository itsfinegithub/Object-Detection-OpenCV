import cv2
from tracker import *

#create tracker object
tracker = EuclideanDistTracker()
cap = cv2.VideoCapture("C:/Users/Lakshmi M/Downloads/object_tracking/object_tracking/highway.mp4")
# object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history = 100, varThreshold = 40)


while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    roi = frame[340: 720,500: 800]
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

# object tracking 

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x,y,w,h,id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    # cv2.imshow("mask", mask)
    key = cv2.waitKey(30) & 0xFF == ord('q')
    if  key ==27:
        break

cap.release()
cv2.destroyAllWindows()