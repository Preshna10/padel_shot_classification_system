from app.utils import get_box_center, euclidean_distance
from app.config import HIT_DISTANCE_THRESHOLD, MIN_SHOT_GAP_FRAMES


class ShotClassifier:
    """
    Rule-based shot classifier.
    Only fires when ball is close to a player AND enough frames
    have passed since the last shot.
    """

    def __init__(self):
        self.last_shot_frame = -999

    def _classify_shot_type(self, ball_center, player_box):
        """
        Classify shot based on ball position relative to player box.
        """
        x1, y1, x2, y2 = player_box
        bx, by         = ball_center

        player_height  = y2 - y1
        player_width   = x2 - x1
        player_cx      = x1 + player_width  / 2
        player_top30   = y1 + player_height * 0.30   # top 30% = head area

        # Ball above head/shoulder → Serve or Smash
        if by <= player_top30:
            return "serve_or_smash"

        # Ball on right side → Forehand
        if bx >= player_cx:
            return "forehand"

        # Ball on left side → Backhand
        return "backhand"

    def detect_shot_event(self, frame_idx, fps, ball_detections, player_tracks):
        """
        Returns a shot dict if a valid shot is detected, else None.
        """
        if not ball_detections or not player_tracks:
            return None

        # Use most confident ball
        ball_det    = ball_detections[0]
        ball_center = get_box_center(ball_det["box"])

        # Find nearest player to the ball
        nearest_pid  = None
        nearest_dist = float("inf")

        for pid, pdata in player_tracks.items():
            d = euclidean_distance(ball_center, pdata["center"])
            if d < nearest_dist:
                nearest_dist = d
                nearest_pid  = pid

        # Ball must be close enough to count as a hit
        if nearest_dist > HIT_DISTANCE_THRESHOLD:
            return None

        # Cooldown: avoid detecting same shot twice
        if frame_idx - self.last_shot_frame < MIN_SHOT_GAP_FRAMES:
            return None

        player_box = player_tracks[nearest_pid]["box"]
        shot_type  = self._classify_shot_type(ball_center, player_box)
        self.last_shot_frame = frame_idx

        return {
            "frame":         frame_idx,
            "timestamp_sec": round(frame_idx / fps, 2),
            "player_id":     nearest_pid,
            "shot_type":     shot_type,
            "ball_x":        ball_center[0],
            "ball_y":        ball_center[1]
        }