import cv2
import numpy as np

# HSV skin range
HSV_LOWER = np.array([0, 30, 60])
HSV_UPPER = np.array([25, 200, 255])

# YCrCb skin range
YCRCB_LOWER = np.array([0, 135, 85])   # [Y, Cr, Cb]
YCRCB_UPPER = np.array([255, 180, 135])

# Area thresholds (absolute, in pixels)
MIN_HAND_AREA = 1200         
MAX_HAND_AREA = 45000        


def get_hand_mask(frame_bgr):
    # HSV mask
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask_hsv = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)

    # YCrCb mask
    ycrcb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2YCrCb)
    mask_ycrcb = cv2.inRange(ycrcb, YCRCB_LOWER, YCRCB_UPPER)

    # Combine: pixel must look like skin in both spaces
    mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)

    # Morphological cleanup
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    return mask


def get_hand_contour_and_centroid(mask, roi=None):

    h, w = mask.shape[:2]

    if roi is None:
        x1, y1, x2, y2 = 0, 0, w, h
    else:
        x1, y1, x2, y2 = roi
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

    roi_mask = mask[y1:y2, x1:x2]

    contours, _ = cv2.findContours(
        roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None, None

    candidates = []

    for c in contours:
        area = cv2.contourArea(c)
        if area < MIN_HAND_AREA or area > MAX_HAND_AREA:
            continue  

        M = cv2.moments(c)
        if M["m00"] == 0:
            continue

        cx_roi = int(M["m10"] / M["m00"])
        cy_roi = int(M["m01"] / M["m00"])

        cx = cx_roi + x1
        cy = cy_roi + y1

        candidates.append((area, c, (cx, cy)))

    if not candidates:
        return None, None

    # Pick largest reasonable skin blob = hand region
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, best_c_roi, best_centroid = candidates[0]

    best_contour = best_c_roi + np.array([[x1, y1]])

    return best_contour, best_centroid
