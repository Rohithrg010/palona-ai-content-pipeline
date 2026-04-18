import os
import json
from datetime import datetime
from pathlib import Path

# Create folders if not exist
OUTPUTS_DIR = Path("outputs")
DATA_DIR = Path("data")

OUTPUTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


def slugify(text):
    return text.lower().replace(" ", "_")


def save_files(content, topic):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slugify(topic)}_{timestamp}"

    # Save JSON
    json_path = OUTPUTS_DIR / f"{filename}.json"
    with open(json_path, "w") as f:
        json.dump(content, f, indent=2)

    # Save Markdown
    md_path = OUTPUTS_DIR / f"{filename}.md"
    with open(md_path, "w") as f:
        f.write(f"# {content['blog_title']}\n\n")
        f.write("## Blog\n\n")
        f.write(content["blog_body"] + "\n\n")

        f.write("## Newsletters\n\n")
        for n in content["newsletters"]:
            f.write(f"### {n['persona']}\n")
            f.write(f"**Subject:** {n['subject_line']}\n\n")
            f.write(n["body"] + "\n\n")
            f.write(f"**CTA:** {n['cta']}\n\n")

    # Save latest content
    latest_path = DATA_DIR / "latest_content.json"
    with open(latest_path, "w") as f:
        json.dump(content, f, indent=2)

    print("✅ Files saved successfully!")


def generate_content(topic):
    print("🚀 Running in MOCK MODE (no API used)")

    content = {
        "topic": topic,
        "blog_title": "How AI is Transforming Creative Automation",
        "blog_outline": [
            "Introduction to AI in creative workflows",
            "Common bottlenecks in agencies",
            "How AI automates repetitive tasks",
            "Real-world use cases",
            "Future of creative automation"
        ],
        "blog_body": "AI is rapidly transforming how creative agencies operate. From automating repetitive design tasks to streamlining client workflows, AI tools are helping teams work faster and smarter. Instead of replacing creativity, AI enhances it by removing manual effort. Agencies can now focus more on strategy and innovation while AI handles routine tasks such as resizing creatives, generating drafts, and organizing assets. This shift allows teams to scale efficiently without sacrificing quality. As AI tools evolve, agencies that adopt early will gain a competitive advantage in both speed and client satisfaction.",
        "newsletters": [
            {
                "persona": "Agency Owners",
                "subject_line": "Scale your agency with AI",
                "body": "Discover how AI can help you take on more clients without increasing headcount. Improve margins and stay competitive with smarter workflows.",
                "cta": "Explore growth strategies"
            },
            {
                "persona": "Operations Managers",
                "subject_line": "Eliminate workflow bottlenecks",
                "body": "Learn how AI can streamline operations, reduce manual work, and improve team coordination across projects.",
                "cta": "Improve efficiency"
            },
            {
                "persona": "Creative Leads",
                "subject_line": "Focus more on creativity",
                "body": "Use AI to handle repetitive tasks and give your team more time to focus on high-quality creative output.",
                "cta": "Boost creativity"
            }
        ]
    }

    save_files(content, topic)
    return content



if __name__ == "__main__":
    topic = "AI in creative automation"
    generate_content(topic)
