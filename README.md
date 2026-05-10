# padel_shot_classification_system
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
