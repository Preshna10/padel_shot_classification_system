import math


def get_box_center(box):
    x1, y1, x2, y2 = box
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def euclidean_distance(p1, p2):
    if p1 is None or p2 is None:
        return float("inf")
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def safe_int(x):
    try:
        return int(x)
    except Exception:
        return 0


def get_box_area(box):
    x1, y1, x2, y2 = box
    return abs((x2 - x1) * (y2 - y1))