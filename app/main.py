import cv2
from tqdm import tqdm

from app.config import (
    INPUT_VIDEO, OUTPUT_VIDEO,
    OUTPUT_CSV, OUTPUT_JSON,
    OUTPUT_ANALYTICS, OUTPUT_CHART
)
from app.io_utils       import ensure_output_dirs, save_shots_csv, save_shots_json, save_analytics_json
from app.detector       import ObjectDetector
from app.tracker        import SimplePlayerTracker
from app.shot_classifier import ShotClassifier
from app.analytics      import build_analytics, save_shot_count_chart
from app.visualizer     import Visualizer


def main():
    print("=" * 60)
    print("  Padel Shot Classification System")
    print("=" * 60)

    ensure_output_dirs(
        OUTPUT_VIDEO, OUTPUT_CSV, OUTPUT_JSON,
        OUTPUT_ANALYTICS, OUTPUT_CHART
    )

    detector   = ObjectDetector()
    tracker    = SimplePlayerTracker()
    classifier = ShotClassifier()
    visualizer = Visualizer()

    print(f"\n[INFO] Opening video: {INPUT_VIDEO}")
    cap = cv2.VideoCapture(str(INPUT_VIDEO))

    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {INPUT_VIDEO}")
        return

    fps          = cap.get(cv2.CAP_PROP_FPS)
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"[INFO] Video info: {width}x{height} @ {fps:.1f} FPS | Total frames: {total_frames}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(OUTPUT_VIDEO), fourcc, fps, (width, height))

    shots     = []
    frame_idx = 0

    print("\n[INFO] Processing frames...\n")

    with tqdm(total=total_frames, desc="Analyzing video",
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections    = detector.detect(frame)
            player_tracks = tracker.update(detections["players"])

            shot = classifier.detect_shot_event(
                frame_idx       = frame_idx,
                fps             = fps,
                ball_detections = detections["balls"],
                player_tracks   = player_tracks
            )

            if shot:
                shots.append(shot)
                visualizer.update_shot(shot)
                tqdm.write(
                    f"  [SHOT DETECTED] Frame {frame_idx:<4} | {shot['shot_type']:>15} | "
                    f"Player {shot['player_id']} | Time {shot['timestamp_sec']}s"
                )

            annotated = visualizer.draw(frame, detections, player_tracks)
            writer.write(annotated)

            frame_idx += 1
            pbar.update(1)

    cap.release()
    writer.release()

    print("\n[INFO] Saving outputs...")
    save_shots_csv(shots,    OUTPUT_CSV)
    save_shots_json(shots,   OUTPUT_JSON)
    save_analytics_json(build_analytics(shots), OUTPUT_ANALYTICS)
    save_shot_count_chart(shots, OUTPUT_CHART)

    print("\n" + "=" * 60)
    print("  PROCESSING COMPLETE")
    print("=" * 60)
    print(f"  Total frames processed : {frame_idx}")
    print(f"  Total shots detected   : {len(shots)}")


if __name__ == "__main__":
    main()