# Padel Game Analytics — Shot Classification System

---

## Project Overview

This system analyzes padel match video footage and automatically:
- Detects and tracks players, ball, and rackets frame by frame
- Classifies shots into 3 types: Forehand, Backhand, Serve/Smash
- Outputs structured results in JSON and CSV format
- Generates analytics summary and bar chart visualization
- Produces annotated output video with bounding boxes and shot labels

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10.13 | Core language |
| YOLOv8n (Ultralytics) | Object detection (players, ball, racket) |
| OpenCV | Video processing and annotation |
| SciPy (Hungarian Algorithm) | Optimal player tracking assignment |
| NumPy / Pandas | Data handling |
| Matplotlib | Shot count bar chart |
| tqdm | Progress bar |

---

## Project Structure

## Project Structure

```text
padel_shot_classification_system/
│
├── app/
│   ├── __init__.py                # Package initialization
│   ├── config.py                  # Configuration settings and paths
│   ├── utils.py                   # Helper utility functions
│   ├── detector.py                # YOLOv8 object detection module
│   ├── tracker.py                 # IoU-based player tracking
│   ├── shot_classifier.py         # Rule-based shot classification
│   ├── analytics.py               # Shot analytics and chart generation
│   ├── visualizer.py              # Video annotation and drawing utilities
│   ├── io_utils.py                # CSV, JSON, and file handling
│   └── main.py                    # Main pipeline entry point
│
├── data/
│   ├── input/
│   │   └── sample_video.mp4       # Input video file
│   │
│   └── output/
│       ├── annotated_output.mp4   # Annotated output video
│       ├── shots.csv              # Shot predictions in CSV format
│       ├── shots.json             # Shot predictions in JSON format
│       ├── analytics_summary.json # Shot statistics summary
│       └── shot_counts.png        # Shot count bar chart
│
├── yolov8n.pt                     # YOLOv8 pretrained model weights
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## Setup Instructions

### Step 1: Clone the Repository

git clone https://github.com/Preshna10/padel_shot_classification_system.git

cd padel_shot_classification_system 

### Step 2: Create Virtual Environment

python -m venv venv

Activate it:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

### Step 3: Install Dependencies

pip install -r requirements.txt

### Step 4: Add Input Video

Place your padel match video inside:

data/input/sample_video.mp4

The filename must be exactly sample_video.mp4

### Step 5: Run the System

python -m app.main

That's it. All output files will be saved automatically in data/output/.

###Methodology

###Stage 1: Object Detection

Used YOLOv8n (pretrained on COCO dataset)

Detects 3 classes per frame:

   Person (class 0) → Players
   
   Sports Ball (class 32) → Padel Ball
   
   Tennis Racket (class 38) → Racket
   
   Confidence threshold set to 0.40

###Stage 2: Player Tracking

Built a custom IoU-based tracker using the Hungarian Algorithm

Tracker maintains consistent Player IDs (1 to 4) across all frames

Uses combined cost metric:

70% weight on IoU (box overlap)

30% weight on centroid distance

Temporal consistency bonus: same player keeps same ID even when partially hidden

Players remembered for up to 120 frames (~5 seconds) when temporarily lost

###Stage 3: Shot Classification (Rule-Based)

When the ball is within 200 pixels of a player AND at least 20 frames

have passed since the last shot, a shot is classified:

Ball Position Relative to Player	Shot Type

Above top 30% of player box (head/shoulder area)	Serve / Smash

Ball center is to the right of player center	Forehand

Ball center is to the left of player center	Backhand

###Stage 4: Output Generation

Annotated video with colored bounding boxes per player

CSV and JSON files with shot type, frame, timestamp, player ID

Analytics summary JSON with total counts per shot type and per player

Bar chart PNG showing shot distribution

Output Format

shots.json

[
  {
    "frame": 87,
    "timestamp_sec": 2.9,
    "player_id": 1,
    "shot_type": "forehand",
    "ball_x": 640,
    "ball_y": 380
  }
]

shots.csv
frame	timestamp_sec	player_id	shot_type	ball_x	ball_y
87	2.9	1	forehand	640	380
143	4.77	2	backhand	420	310

analytics_summary.json

{
  "total_shots": 12,
  "shot_type_counts": {
    "forehand": 5,
    "backhand": 4,
    "serve_or_smash": 3
  },
  "player_shot_counts": {
    "Player 1": 7,
    "Player 2": 5
  }
}


###Bonus Features Completed ✅

✅ Shot count analytics (forehand vs backhand vs serve/smash)

✅ Visual overlay on output video (colored boxes, shot banner, labels)

✅ Bar chart dashboard (shot_counts.png)

✅ Rule-based shot direction logic (left/right/above relative to player)

✅ Cooldown logic to prevent duplicate shot detection

###Demo Video
Click here to watch the demo

###Models

YOLOv8n pretrained model used for detection.

Download Model from Google Drive

###Challenges Faced

1.Ball Detection Gaps

YOLOv8n (COCO) detects sports balls but padel balls are small and fast

Solution: Lowered confidence threshold to 0.40 and used closest ball to player

Player ID Switching

2.When players cross paths, IDs would swap

Solution: Built IoU + Hungarian Algorithm tracker with temporal consistency

bonus to keep IDs stable

False Shot Detection

3.Ball passing near a player without a hit was triggering shots

Solution: Added 20-frame cooldown between shots and 200px distance threshold

No Padel-Specific Dataset

4.No labeled padel dataset available for fine-tuning

Solution: Used COCO pretrained YOLOv8n which detects persons,

sports balls, and tennis rackets — close enough for a working prototype

###Improvements I Would Make

Fine-tune YOLO on padel-specific data for much better ball and racket detection

Use pose estimation (MediaPipe) to classify shots by arm angle,
not just ball position — much more accurate

Audio analysis — racket hit makes a distinct sound,
could use it as a trigger for shot detection

Player identification using jersey color or number detection

Court homography — map player positions to a 2D court top-view
for shot direction tracking

Real-time inference — optimize with ONNX or TensorRT for live video

Requirements
See requirements.txt:

text

ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
scipy>=1.10.0
tqdm>=4.65.0
text


faced, and what you would improve — which is exactly what they are evaluating. 🎯

