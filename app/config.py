from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_VIDEO      = BASE_DIR / "data" / "input"  / "sample_video.mp4"
OUTPUT_VIDEO     = BASE_DIR / "data" / "output" / "annotated_output.mp4"
OUTPUT_CSV       = BASE_DIR / "data" / "output" / "shots.csv"
OUTPUT_JSON      = BASE_DIR / "data" / "output" / "shots.json"
OUTPUT_ANALYTICS = BASE_DIR / "data" / "output" / "analytics_summary.json"
OUTPUT_CHART     = BASE_DIR / "data" / "output" / "shot_counts.png"

YOLO_MODEL = "yolov8n.pt"

CONF_THRESHOLD         = 0.40
PERSON_CLASS_ID        = 0
SPORTS_BALL_CLASS_ID   = 32
TENNIS_RACKET_CLASS_ID = 38

MAX_PLAYERS = 4

# Tracker settings
TRACKER_MAX_DISTANCE    = 400   # pixels - max allowed centroid shift per frame
TRACKER_MAX_DISAPPEARED = 120   # frames - remember player for ~5 seconds at 25fps

# Shot detection
HIT_DISTANCE_THRESHOLD = 200
MIN_SHOT_GAP_FRAMES    = 20