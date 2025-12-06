import cv2

def draw_virtual_rect(frame, rect, state):
    
    (x1, y1, x2, y2) = rect

    if state == "DANGER":
        color = (0, 0, 255)       # red
    elif state == "WARNING":
        color = (0, 165, 255)     # orange
    elif state == "NO_HAND":
        color = (200, 200, 200)     # yellow
    else:
        color = (0, 255, 255)     # yellow

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)


def draw_state_panel(frame, state, distance):
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (260, 70), (0, 0, 0), -1)
    frame[:] = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    # State-dependent text color
    if state == "SAFE":
        color = (0, 255, 0)
    elif state == "WARNING":
        color = (0, 255, 255)
    elif state == "DANGER":
        color = (0, 0, 255)
    else:
        color = (255, 255, 255)

    cv2.putText(
        frame,
        f"STATE: {state}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2,
    )

    # Distance text 
    if distance is not None:
        cv2.putText(
            frame,
            f"Distance: {distance:.1f}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
        )


def draw_danger_warning(frame, state):
    
    if state == "DANGER":
        cv2.putText(
            frame,
            "DANGER DANGER",
            (120, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.4,
            (0, 0, 255),
            3,
        )
