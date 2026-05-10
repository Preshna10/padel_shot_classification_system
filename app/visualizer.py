import cv2
from app.utils import safe_int

COLOR_PLAYER  = (0,   255,   0)
COLOR_BALL    = (0,   0,   255)
COLOR_RACKET  = (255, 128,   0)
COLOR_SHOT    = (0,   255, 255)

# Player ID → unique color so each player has own color box
PLAYER_COLORS = {
    1: (0,   255,   0),    # Green
    2: (255,  0,    0),    # Blue
    3: (0,   0,   255),    # Red
    4: (255, 255,   0),    # Cyan
}

SHOT_DISPLAY_FRAMES = 40   # how many frames to show the shot label


class Visualizer:
    def __init__(self):
        self.current_shot      = None
        self.shot_display_left = 0

    def update_shot(self, shot):
        if shot:
            self.current_shot      = shot
            self.shot_display_left = SHOT_DISPLAY_FRAMES

    def draw(self, frame, detections, player_tracks):
        # Draw player bounding boxes with unique colors
        for pid, pdata in player_tracks.items():
            x1, y1, x2, y2 = map(safe_int, pdata["box"])
            color = PLAYER_COLORS.get(pid, (200, 200, 200))

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            label = f"Player {pid}"
            (tw, th), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
            cv2.rectangle(frame,
                          (x1, y1 - th - 10),
                          (x1 + tw + 6, y1),
                          color, -1)
            cv2.putText(frame, label,
                        (x1 + 3, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 0, 0), 2)

        # Draw ball
        for det in detections["balls"]:
            x1, y1, x2, y2 = map(safe_int, det["box"])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            r  = max((x2 - x1), (y2 - y1)) // 2
            cv2.circle(frame, (cx, cy), max(r, 8), COLOR_BALL, 2)
            cv2.putText(frame, "Ball",
                        (cx - 15, cy - r - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, COLOR_BALL, 2)

        # Draw rackets
        for det in detections["rackets"]:
            x1, y1, x2, y2 = map(safe_int, det["box"])
            cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_RACKET, 2)
            cv2.putText(frame, "Racket",
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, COLOR_RACKET, 2)

        # Draw shot banner
        if self.shot_display_left > 0 and self.current_shot:
            self._draw_shot_banner(frame, self.current_shot)
            self.shot_display_left -= 1

        return frame

    def _draw_shot_banner(self, frame, shot):
        shot_label  = shot["shot_type"].upper().replace("_", " ")
        line1 = f"SHOT DETECTED:  {shot_label}"
        line2 = f"Player {shot['player_id']}   |   {shot['timestamp_sec']}s"

        cv2.rectangle(frame, (0, 0), (frame.shape[1], 70), (0, 0, 0), -1)
        cv2.putText(frame, line1,
                    (15, 32),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, COLOR_SHOT, 2)
        cv2.putText(frame, line2,
                    (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (200, 200, 200), 1)