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


