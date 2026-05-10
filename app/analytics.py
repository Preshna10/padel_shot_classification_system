from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def build_analytics(shots):
    if not shots:
        return {
            "total_shots":        0,
            "shot_type_counts":   {},
            "player_shot_counts": {}
        }

    shot_types   = [s["shot_type"]      for s in shots]
    player_ids   = [f"Player {s['player_id']}" for s in shots]

    return {
        "total_shots":        len(shots),
        "shot_type_counts":   dict(Counter(shot_types)),
        "player_shot_counts": dict(Counter(player_ids))
    }


def save_shot_count_chart(shots, output_path):
    if not shots:
        print("[WARNING] No shots — skipping chart.")
        return

    counts = Counter(s["shot_type"] for s in shots)
    labels = list(counts.keys())
    values = list(counts.values())

    colors = {
        "forehand":       "#4CAF50",
        "backhand":       "#2196F3",
        "serve_or_smash": "#FF5722"
    }
    bar_colors = [colors.get(l, "#9C27B0") for l in labels]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=bar_colors, edgecolor="black")

    for bar, val in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(val),
            ha="center", va="bottom",
            fontsize=12, fontweight="bold"
        )

    plt.title("Shot Type Distribution", fontsize=15, fontweight="bold")
    plt.xlabel("Shot Type", fontsize=12)
    plt.ylabel("Count",     fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"[INFO] Chart saved: {output_path}")