import cv2
import time

from hand_detector import get_hand_mask, get_hand_contour_and_centroid
from interaction_logic import classify_state
from overlay import draw_virtual_rect, draw_state_panel, draw_danger_warning


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab initial frame.")
        return

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

   
    # 1. Virtual rectangle (DANGER zone)
   
    rect_w, rect_h = 150, 120
    rect_x2 = int(w * 0.88)
    rect_y2 = int(h * 0.85)
    rect_x1 = rect_x2 - rect_w
    rect_y1 = rect_y2 - rect_h
    virtual_rect = (rect_x1, rect_y1, rect_x2, rect_y2)

    
    # 2. Face detector (to remove face from skin mask)
   
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if face_cascade.empty():
        print("Error: Could not load Haar cascade for face detection.")
        return

    prev_time = time.time()
    print("Press 'q' or ESC to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 1) Skin mask (HSV + YCrCb)
        skin_mask = get_hand_mask(frame)

        # 2) Detect face and remove from mask
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (fx, fy, fw, fh) in faces:
            skin_mask[fy:fy + fh, fx:fx + fw] = 0

        # 3) Detect hand on the FULL FRAME (no ROI restriction)
        contour, centroid = get_hand_contour_and_centroid(skin_mask, roi=None)


        if contour is not None:
            cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)

        if centroid is not None:
            cx, cy = centroid
            cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
            cv2.putText(frame, f"({cx},{cy})", (cx + 10, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # 4) State classification:
        #    - NO_HAND: no skin contour at all
        #    - SAFE   : hand detected, far from virtual_rect
        #    - WARNING: hand closer
        #    - DANGER : hand touching virtual_rect
        state, distance = classify_state(contour, centroid, virtual_rect)

        # 5) Draw virtual rect + state overlays
        draw_virtual_rect(frame, virtual_rect, state)
        draw_state_panel(frame, state, distance)
        draw_danger_warning(frame, state)

        # FPS 
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if curr_time != prev_time else 0.0
        prev_time = curr_time
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (frame.shape[1] - 140, 25),        
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        cv2.imshow("Skin Mask (Face Removed)", skin_mask)
        cv2.imshow("Hand Interaction", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in [27, ord('q')]:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
