import json
import pandas as pd
from pathlib import Path


def ensure_output_dirs(*paths):
    for path in paths:
        Path(path).parent.mkdir(parents=True, exist_ok=True)


def save_shots_csv(shots, output_path):
    if not shots:
        df = pd.DataFrame(columns=[
            "frame", "timestamp_sec", "player_id",
            "shot_type", "ball_x", "ball_y"])
    else:
        df = pd.DataFrame(shots)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Shots CSV saved: {output_path}")


def save_shots_json(shots, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(shots, f, indent=2)
    print(f"[INFO] Shots JSON saved: {output_path}")


def save_analytics_json(analytics, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analytics, f, indent=2)
    print(f"[INFO] Analytics JSON saved: {output_path}")