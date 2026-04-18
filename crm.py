import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def load_contacts():
    contacts_path = DATA_DIR / "contacts.json"
    if not contacts_path.exists():
        return []

    with open(contacts_path, "r") as f:
        return json.load(f)


def load_latest_content():
    latest_path = DATA_DIR / "latest_content.json"
    with open(latest_path, "r") as f:
        return json.load(f)


def segment_contacts_by_persona(contacts):
    segmented = {}
    for contact in contacts:
        persona = contact["persona"]
        if persona not in segmented:
            segmented[persona] = []
        segmented[persona].append(contact)
    return segmented


def match_newsletters_to_personas(newsletters):
    return {newsletter["persona"]: newsletter for newsletter in newsletters}


def log_campaign(campaign_entry):
    log_path = DATA_DIR / "campaign_log.json"

    if log_path.exists():
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(campaign_entry)

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)


def run_crm_workflow():
    contacts = load_contacts()
    content = load_latest_content()

    segmented_contacts = segment_contacts_by_persona(contacts)
    newsletter_map = match_newsletters_to_personas(content["newsletters"])

    campaign_id = f"camp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    for persona, persona_contacts in segmented_contacts.items():
        newsletter = newsletter_map.get(persona)

        if newsletter:
            campaign_entry = {
                "campaign_id": campaign_id,
                "blog_title": content["blog_title"],
                "persona": persona,
                "newsletter_subject": newsletter["subject_line"],
                "send_date": datetime.now().isoformat(),
                "recipient_count": len(persona_contacts),
                "recipients": [contact["email"] for contact in persona_contacts]
            }
            log_campaign(campaign_entry)
            print(f"Sent newsletter to {persona}: {len(persona_contacts)} contact(s)")

    print("CRM workflow completed successfully.")


if __name__ == "__main__":
    run_crm_workflow()
