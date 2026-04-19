import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUTS_DIR = Path("outputs")
DATA_DIR = Path("data")

OUTPUTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

def slugify(text):
    return text.lower().replace(" ", "_")

def save_files(content, topic):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slugify(topic)}_{timestamp}"
    json_path = OUTPUTS_DIR / f"{filename}.json"
    with open(json_path, "w") as f:
        json.dump(content, f, indent=2)
    md_path = OUTPUTS_DIR / f"{filename}.md"
    with open(md_path, "w") as f:
        f.write(f"# {content['blog_title']}\n\n")
        f.write(content["blog_body"] + "\n\n")
        for n in content["newsletters"]:
            f.write(f"### {n['persona']}\n")
            f.write(f"**Subject:** {n['subject_line']}\n\n")
            f.write(n["body"] + "\n\n")
    latest_path = DATA_DIR / "latest_content.json"
    with open(latest_path, "w") as f:
        json.dump(content, f, indent=2)
    print("Files saved!")

def generate_content(topic):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("No API key — mock mode")
        return _mock_content(topic)

    print(f"Generating content for: {topic}")
    prompt = f"""You are a content strategist for NovaMind, an AI startup for creative agencies.
Generate a JSON object for topic: "{topic}"
Return ONLY valid JSON, no markdown, no backticks:
{{
  "topic": "{topic}",
  "blog_title": "compelling SEO title",
  "blog_outline": ["Section 1", "Section 2", "Section 3", "Section 4"],
  "blog_body": "400-500 word blog post with specific examples and insights",
  "newsletters": [
    {{"persona": "Agency Owners", "subject_line": "subject for agency owners", "body": "150 word newsletter focused on ROI and scaling", "cta": "CTA text"}},
    {{"persona": "Operations Managers", "subject_line": "subject for ops managers", "body": "150 word newsletter focused on efficiency", "cta": "CTA text"}},
    {{"persona": "Creative Leads", "subject_line": "subject for creative leads", "body": "150 word newsletter focused on creative freedom", "cta": "CTA text"}}
  ]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a marketing expert. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        content = json.loads(raw)
        save_files(content, topic)
        print("Content generated successfully!")
        return content
    except Exception as e:
        print(f"API error: {e} — using mock")
        return _mock_content(topic)

def _mock_content(topic):
    content = {
        "topic": topic,
        "blog_title": f"How AI is Transforming {topic.title()}",
        "blog_outline": ["Introduction", "Key Benefits", "Use Cases", "Getting Started"],
        "blog_body": f"AI is rapidly transforming how creative agencies approach {topic}. From automating repetitive design tasks to streamlining client workflows, AI tools are helping teams work faster and smarter. Instead of replacing creativity, AI enhances it by removing manual effort. Agencies can now focus more on strategy and innovation while AI handles routine tasks. This shift allows teams to scale efficiently without sacrificing quality.",
        "newsletters": [
            {"persona": "Agency Owners", "subject_line": f"Scale your agency with {topic}", "body": f"Discover how {topic} helps agency owners take on more clients without increasing headcount.", "cta": "Explore now"},
            {"persona": "Operations Managers", "subject_line": f"Eliminate bottlenecks with {topic}", "body": f"Learn how {topic} streamlines operations and reduces manual work across projects.", "cta": "Learn more"},
            {"persona": "Creative Leads", "subject_line": f"More creativity with {topic}", "body": f"Use {topic} to handle repetitive tasks and focus on high-quality creative output.", "cta": "Get started"}
        ]
    }
    save_files(content, topic)
    return content

if __name__ == "__main__":
    topic = "AI in creative automation"
    generate_content(topic)
