import cv2

min_area_threshold = 1000  # You can adjust the value as needed

def find_contour_detector(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 100, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_detectors = []

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            contour_area = cv2.contourArea(approx)

            if contour_area > min_area_threshold:
                contour_detectors.append((x, y, w, h))

    if len(contour_detectors) >= 1:
        return contour_detectors

    return None
