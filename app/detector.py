from ultralytics import YOLO
from app.config import (
    YOLO_MODEL,
    CONF_THRESHOLD,
    PERSON_CLASS_ID,
    SPORTS_BALL_CLASS_ID,
    TENNIS_RACKET_CLASS_ID
)


class ObjectDetector:
    def __init__(self):
        self.model = YOLO(YOLO_MODEL)

    def detect(self, frame):
        results = self.model(frame, conf=CONF_THRESHOLD, verbose=False)

        detections = {
            "players": [],
            "balls":   [],
            "rackets": []
        }

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                conf   = float(box.conf[0].item())
                xyxy   = box.xyxy[0].cpu().numpy().tolist()

                det = {
                    "box":      xyxy,
                    "conf":     round(conf, 2),
                    "class_id": cls_id
                }

                if cls_id == PERSON_CLASS_ID:
                    detections["players"].append(det)
                elif cls_id == SPORTS_BALL_CLASS_ID:
                    detections["balls"].append(det)
                elif cls_id == TENNIS_RACKET_CLASS_ID:
                    detections["rackets"].append(det)

        return detections