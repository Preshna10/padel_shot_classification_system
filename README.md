# Padel Game Analytics — Shot Classification System
### AI/ML Internship Assignment | Layman AI

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
| Python 3.10+ | Core language |
| YOLOv8n (Ultralytics) | Object detection (players, ball, racket) |
| OpenCV | Video processing and annotation |
| SciPy (Hungarian Algorithm) | Optimal player tracking assignment |
| NumPy / Pandas | Data handling |
| Matplotlib | Shot count bar chart |
| tqdm | Progress bar |

---

## Project Structure
padel_shot_classification_system/
│
├── app/
│ ├── init.py # Package init
│ ├── config.py # All settings and paths
│ ├── utils.py # Helper functions
│ ├── detector.py # YOLOv8 object detection
│ ├── tracker.py # IoU-based player tracker
│ ├── shot_classifier.py # Rule-based shot classification
│ ├── analytics.py # Shot count analytics + chart
│ ├── visualizer.py # Video annotation/drawing
│ ├── io_utils.py # Save CSV, JSON, files
│ └── main.py # Main pipeline entry point
│
├── data/
│ ├── input/
│ │ └── sample_video.mp4 ← Place your input video here
│ └── output/
│ ├── annotated_output.mp4 ← Output video with overlays
│ ├── shots.csv ← Shot predictions table
│ ├── shots.json ← Shot predictions JSON
│ ├── analytics_summary.json← Shot counts summary
│ └── shot_counts.png ← Bar chart visualization
├── yolov8n.pt  
├── requirements.txt
└── README.md


---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/padel-shot-classification-system.git
cd padel-shot-classification-system 

Step 2: Create Virtual Environment
python -m venv venv

Activate it:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Add Input Video
Place your padel match video inside:

data/input/sample_video.mp4
The filename must be exactly sample_video.mp4

Step 5: Run the System

python -m app.main
That's it. All output files will be saved automatically in data/output/


