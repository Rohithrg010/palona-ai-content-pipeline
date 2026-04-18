import json
import random
from pathlib import Path

DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")

DATA_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)


def load_campaign_logs():
    log_path = DATA_DIR / "campaign_log.json"
    if not log_path.exists():
        return []

    with open(log_path, "r") as f:
        return json.load(f)


def simulate_performance(logs):
    performance_data = []

    for log in logs:
        performance = {
            "campaign_id": log["campaign_id"],
            "persona": log["persona"],
            "open_rate": round(random.uniform(0.35, 0.55), 2),
            "click_rate": round(random.uniform(0.10, 0.30), 2),
            "unsubscribe_rate": round(random.uniform(0.00, 0.05), 2)
        }
        performance_data.append(performance)

    return performance_data


def save_performance(performance_data):
    history_path = DATA_DIR / "performance_history.json"
    with open(history_path, "w") as f:
        json.dump(performance_data, f, indent=2)


def generate_summary(performance_data):
    best_persona = max(performance_data, key=lambda x: x["click_rate"])

    summary = {
        "best_persona": best_persona["persona"],
        "summary": f"{best_persona['persona']} had the highest click rate at {best_persona['click_rate']}. This audience responded best to the newsletter message.",
        "recommendation": f"Create more content tailored to {best_persona['persona']} and test similar messaging in future campaigns.",
        "next_topic_idea": "How AI helps creative teams move faster without losing quality"
    }

    summary_path = OUTPUTS_DIR / "performance_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("Performance summary saved.")


def generate_markdown_report(performance_data):
    report_path = OUTPUTS_DIR / "campaign_report.md"

    best = max(performance_data, key=lambda x: x["click_rate"])

    with open(report_path, "w") as f:
        f.write("# 📊 Campaign Performance Report\n\n")

        f.write("## 🏆 Best Performing Persona\n")
        f.write(f"- {best['persona']} (Click Rate: {best['click_rate']})\n\n")

        f.write("## 📈 Metrics by Persona\n")
        for p in performance_data:
            f.write(f"### {p['persona']}\n")
            f.write(f"- Open Rate: {p['open_rate']}\n")
            f.write(f"- Click Rate: {p['click_rate']}\n")
            f.write(f"- Unsubscribe Rate: {p['unsubscribe_rate']}\n\n")

        f.write("## 💡 Insights\n")
        f.write(f"{best['persona']} responded best. Focus more content on this audience.\n\n")

        f.write("## 🚀 Next Content Idea\n")
        f.write("How AI helps creative teams scale without burnout\n")

    print("Markdown report created.")


def run_analysis():
    logs = load_campaign_logs()
    performance_data = simulate_performance(logs)
    save_performance(performance_data)
    generate_summary(performance_data)
    generate_markdown_report(performance_data)
    print("Analysis completed successfully.")


if __name__ == "__main__":
    run_analysis()
