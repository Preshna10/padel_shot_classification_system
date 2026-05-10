import numpy as np
from scipy.optimize import linear_sum_assignment
from collections import OrderedDict

from app.utils import get_box_center
from app.config import TRACKER_MAX_DISTANCE, TRACKER_MAX_DISAPPEARED


def iou(boxA, boxB):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.
    IoU is much more robust than centroid distance for tracking.
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0.0

    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    iou_score = interArea / float(boxAArea + boxBArea - interArea)
    return iou_score


class SimplePlayerTracker:
    """
    IoU-based tracker with temporal consistency.
    
    This tracker:
    1. Uses IoU (box overlap) as primary matching metric
    2. Adds centroid distance as secondary metric
    3. Strongly prefers keeping the same player ID across frames (temporal consistency)
    4. Uses Hungarian algorithm for optimal global assignment
    5. Maintains strict IDs 1-4 only
    """

    def __init__(self):
        self.tracks = OrderedDict()      # {id: {"box": ..., "center": ...}}
        self.disappeared = OrderedDict() # {id: frames_missing}
        self.last_match = OrderedDict()  # {id: last_detection_index_matched}
        
        self.max_distance = TRACKER_MAX_DISTANCE
        self.max_gone = TRACKER_MAX_DISAPPEARED
        self.available_ids = [1, 2, 3, 4]

    def _register(self, box, center):
        if len(self.available_ids) == 0:
            return
        new_id = min(self.available_ids)
        self.available_ids.remove(new_id)
        
        self.tracks[new_id] = {"box": box, "center": center}
        self.disappeared[new_id] = 0
        self.last_match[new_id] = -1

    def _deregister(self, tid):
        del self.tracks[tid]
        del self.disappeared[tid]
        del self.last_match[tid]
        if tid not in self.available_ids:
            self.available_ids.append(tid)

    def update(self, player_detections):
        # Case: No detections this frame
        if len(player_detections) == 0:
            for tid in list(self.disappeared.keys()):
                self.disappeared[tid] += 1
                if self.disappeared[tid] > self.max_gone:
                    self._deregister(tid)
            return {tid: data for tid, data in self.tracks.items() 
                    if self.disappeared[tid] == 0}

        input_boxes = [d["box"] for d in player_detections]
        input_centers = [get_box_center(b) for b in input_boxes]

        # Case: No existing tracks
        if len(self.tracks) == 0:
            for i in range(len(input_boxes)):
                self._register(input_boxes[i], input_centers[i])
            return {tid: data for tid, data in self.tracks.items() 
                    if self.disappeared[tid] == 0}

        track_ids = list(self.tracks.keys())
        num_tracks = len(track_ids)
        num_dets = len(input_boxes)

        # Build cost matrix: lower cost = better match
        # Cost = (1 - IoU) * 0.7 + normalized_centroid_dist * 0.3
        cost_matrix = np.full((num_tracks, num_dets), 9999.0)

        for r, tid in enumerate(track_ids):
            track_box = self.tracks[tid]["box"]
            track_center = self.tracks[tid]["center"]

            for c in range(num_dets):
                det_box = input_boxes[c]
                det_center = input_centers[c]

                # IoU component (primary)
                iou_score = iou(track_box, det_box)
                
                # Centroid distance component (secondary)
                centroid_dist = np.sqrt(
                    (track_center[0] - det_center[0])**2 + 
                    (track_center[1] - det_center[1])**2
                )
                
                # Normalize centroid distance (0-1 range roughly)
                norm_centroid = min(centroid_dist / self.max_distance, 1.0)
                
                # Combined cost: IoU is more important
                cost = (1.0 - iou_score) * 0.7 + norm_centroid * 0.3
                
                # TEMPORAL CONSISTENCY BONUS:
                # If this track was matched to this detection in the previous frame,
                # give it a strong advantage (lower cost)
                if self.last_match[tid] == c:
                    cost -= 0.5  # Strong preference to keep same assignment
                
                cost_matrix[r, c] = max(cost, 0.0)

        # Hungarian algorithm for optimal assignment
        row_indices, col_indices = linear_sum_assignment(cost_matrix)

        used_rows = set()
        used_cols = set()

        for row, col in zip(row_indices, col_indices):
            # Reject if cost is too high (no good match)
            if cost_matrix[row, col] > 1.5:
                continue

            tid = track_ids[row]
            self.tracks[tid]["box"] = input_boxes[col]
            self.tracks[tid]["center"] = input_centers[col]
            self.disappeared[tid] = 0
            self.last_match[tid] = col  # Remember this match for next frame

            used_rows.add(row)
            used_cols.add(col)

        # Handle unmatched tracks (player temporarily lost)
        for row in range(num_tracks):
            if row not in used_rows:
                tid = track_ids[row]
                self.disappeared[tid] += 1
                self.last_match[tid] = -1  # Clear last match
                
                if self.disappeared[tid] > self.max_gone:
                    self._deregister(tid)

        # Handle unmatched detections (new player appeared)
        for col in range(num_dets):
            if col not in used_cols:
                self._register(input_boxes[col], input_centers[col])

        # Return only currently visible players
        return {tid: data for tid, data in self.tracks.items() 
                if self.disappeared[tid] == 0}