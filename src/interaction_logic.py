import math

DANGER_DIST = 40     # touching
WARNING_DIST = 150   # approaching


def distance_point_to_rect(px, py, x1, y1, x2, y2):
    dx = max(x1 - px, 0, px - x2)
    dy = max(y1 - py, 0, py - y2)
    return math.sqrt(dx * dx + dy * dy)


def contour_intersects_rect(contour, x1, y1, x2, y2):
    if contour is None:
        return False
    for p in contour:
        x, y = p[0]
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False


def classify_state(contour, centroid, rect):
    (x1, y1, x2, y2) = rect

    # 1) No hand detected near ROI
    if contour is None or centroid is None:
        return "NO_HAND", None

    cx, cy = centroid

    # 2) Direct contact with virtual object
    if contour_intersects_rect(contour, x1, y1, x2, y2):
        return "DANGER", 0.0

    # 3) Distance-based SAFE/WARNING
    d = distance_point_to_rect(cx, cy, x1, y1, x2, y2)

    if d < DANGER_DIST:
        return "DANGER", d
    elif d < WARNING_DIST:
        return "WARNING", d
    else:
        return "SAFE", d
