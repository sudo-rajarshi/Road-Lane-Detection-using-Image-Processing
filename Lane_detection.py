import cv2
import numpy as np


def edges(image):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_yellow = np.array([18, 94, 140], dtype="uint8")
    high_yellow = np.array([48, 255, 255], dtype="uint8")

    mask_yellow = cv2.inRange(hsv, low_yellow, high_yellow)
    edges = cv2.Canny(mask_yellow, 75, 150)

    return edges


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return line_image


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(500, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


cap = cv2.VideoCapture("road_car_view.mp4")
while True:
    ret, frame = cap.read()
    if not ret:

        cap = cv2.VideoCapture("road_car_view.mp4")
        continue
    canny_image = edges(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 1, np.pi / 180, 50, maxLineGap=50)
    line_image = display_lines(frame, lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()