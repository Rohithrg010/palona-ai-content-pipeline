import json
import os
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = "https://api.hubapi.com"

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}

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

def batch_create_hubspot_contacts(contacts):
    if not HUBSPOT_API_KEY:
        print("No HubSpot API key — using mock mode")
        return None
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/batch/create"
    inputs = []
    for contact in contacts[:10]:
        inputs.append({
            "properties": {
                "email": contact.get("email"),
                "firstname": contact.get("name", "User"),
                "jobtitle": contact.get("persona", ""),
            }
        })
    try:
        response = requests.post(url, headers=HEADERS, json={"inputs": inputs})
        if response.status_code in [200, 201]:
            print(f"HubSpot: {len(inputs)} contacts created")
            return response.json()
        else:
            print(f"HubSpot error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"HubSpot API error: {e}")
        return None

def run_crm_workflow():
    contacts = load_contacts()
    content = load_latest_content()
    segmented_contacts = segment_contacts_by_persona(contacts)
    newsletter_map = match_newsletters_to_personas(content["newsletters"])
    campaign_id = f"camp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if HUBSPOT_API_KEY:
        batch_create_hubspot_contacts(contacts)
    else:
        print("Mock mode — add HUBSPOT_API_KEY to .env for real API calls")

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
                "recipients": [c["email"] for c in persona_contacts]
            }
            log_campaign(campaign_entry)
            print(f"Sent to {persona}: {len(persona_contacts)} contact(s)")

    print("CRM workflow completed successfully.")
    return campaign_id

if __name__ == "__main__":
    run_crm_workflow()
