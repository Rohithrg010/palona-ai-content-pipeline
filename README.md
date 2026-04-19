# NovaMind AI Content Pipeline

> An end-to-end AI-powered marketing pipeline that generates, distributes, and analyzes blog and newsletter content — built for the Palona AI take-home assignment.

🚀 **Live Demo:** https://novamind-pipeline.streamlit.app  
📂 **GitHub:** https://github.com/Rohithrg010/palona-ai-content-pipeline

---

## What It Does

NovaMind is a fictional early-stage AI startup that helps small creative agencies automate their daily workflows. This pipeline automates their entire weekly content workflow:

1. **Generate** — Takes a blog topic and uses AI to produce a full blog post + 3 personalized newsletters (one per audience segment)
2. **Distribute** — Segments contacts by persona and dispatches campaigns via real HubSpot CRM API calls
3. **Analyze** — Tracks open rates, click rates, and unsubscribe rates across segments with visual charts
4. **Optimize** — Uses AI to generate performance insights and suggest next week's content topics

---

## Live Demo

Visit the live app — no installation required:

```
https://novamind-pipeline.streamlit.app
```

To use the app:
1. Go to **✦ Generate Content** — type any topic and click Generate
2. Go to **⬡ CRM & Distribution** — click Dispatch Campaign
3. Go to **◈ Analytics** — view charts and click Generate AI Insight
4. Go to **◎ AI Optimizer** — get next topic suggestions
5. Go to **≡ Campaign History** — view all past campaigns

---

## Architecture

```
User Input (Topic)
       ↓
OpenAI GPT-4o-mini API
       ↓
Blog Post (400-500 words) + 3 Persona Newsletters → JSON
       ↓
Saved to: outputs/ (JSON + Markdown) + data/latest_content.json
       ↓
HubSpot CRM API
  POST /crm/v3/objects/contacts/batch/create  (segment contacts)
  POST /marketing/v3/emails                    (log campaign)
       ↓
Performance Analytics (open rate, click rate, unsubscribe rate)
       ↓
AI Performance Insight + Next Topic Suggestions
```

---

## Target Personas

| Persona | Description | Newsletter Focus |
|---|---|---|
| 🟣 Agency Owners | Agency owners who manage creative teams | ROI, scaling, competitive advantage |
| 🟢 Operations Managers | Ops managers handling workflows | Efficiency, bottlenecks, coordination |
| 🟡 Creative Leads | Creative directors and leads | Creative freedom, quality, less busywork |

---

## Tech Stack

| Component | Tool |
|---|---|
| AI Content Generation | OpenAI GPT-4o-mini |
| CRM Integration | HubSpot v3 API (real API calls) |
| Frontend Dashboard | Streamlit |
| Charts & Analytics | Plotly |
| Data Storage | JSON files |
| Deployment | Streamlit Cloud |
| Language | Python 3 |

---

## Features

- **AI Blog Generation** — Full 400-500 word blog post with outline from a single topic input
- **3 Persona Newsletters** — Each newsletter customized in tone and focus for a different audience
- **Real HubSpot Integration** — Batch creates contacts, segments by persona, logs campaigns via v3 API
- **Performance Dashboard** — Open rate, click rate, unsubscribe rate with interactive Plotly charts
- **AI Performance Insight** — Analyzes campaign data and gives specific recommendations
- **Topic Optimizer** — Suggests next blog topics based on engagement trends
- **Headline A/B Generator** — Rewrites headlines using 5 copywriting techniques
- **Campaign History** — Full log of all past campaigns with performance snapshots
- **Fallback Mock Mode** — App works even without API keys for demo purposes

---

## Project Structure

```
palona-ai-content-pipeline/
├── app.py                    ← Streamlit dashboard (main UI)
├── generate_content.py       ← OpenAI content generation
├── crm.py                    ← HubSpot CRM integration
├── analysis.py               ← Performance analytics engine
├── main.py                   ← Pipeline orchestrator (CLI)
├── requirements.txt          ← Python dependencies
├── data/
│   ├── contacts.json         ← Seeded mock contact data
│   ├── campaign_log.json     ← All campaign records
│   ├── latest_content.json   ← Most recently generated content
│   └── performance_history.json
└── outputs/                  ← Generated blog/newsletter files (JSON + MD)
```

---

## How to Run Locally

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/Rohithrg010/palona-ai-content-pipeline.git
cd palona-ai-content-pipeline
```

**Step 2 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 3 — Create a .env file:**
```bash
touch .env
```

Add your API keys (app works in mock mode without these):
```
OPENAI_API_KEY=your-openai-key-here
HUBSPOT_API_KEY=your-hubspot-private-app-token-here
```

**Step 4 — Run the dashboard:**
```bash
streamlit run app.py
```

**Step 5 — Open in browser:**
```
http://localhost:8501
```

---

## HubSpot API Integration

The system uses HubSpot's free developer account with v3 CRM API.

**Endpoints used:**

```
POST /crm/v3/objects/contacts/batch/create
  → Batch creates and segments contacts by persona

POST /marketing/v3/emails
  → Logs campaign dispatch with newsletter metadata

GET /crm/v3/objects/contacts
  → Fetches existing contacts for deduplication
```

**Example contact payload:**
```json
{
  "inputs": [
    {
      "properties": {
        "email": "sarah.creative@novamind.ai",
        "firstname": "Sarah",
        "lastname": "Creative",
        "jobtitle": "Agency Owner",
        "hs_lead_status": "NEW"
      }
    }
  ]
}
```

---

## ✅ API Testing — Verified with Postman

The HubSpot CRM API integration was fully tested and verified using Postman.

**Test: Create Contact via HubSpot v3 API**

- **Method:** POST
- **Endpoint:** `https://api.hubapi.com/crm/v3/objects/contacts/batch/create`
- **Auth:** Bearer Token (HubSpot Private App)
- **Result:** ✅ 201 Created — contact successfully created in HubSpot

**Postman Response:**
```json
{
  "status": "COMPLETE",
  "results": [
    {
      "id": "473551108829",
      "properties": {
        "email": "sarah.creative@novamind.ai",
        "firstname": "Sarah",
        "lastname": "Creative",
        "jobtitle": "Agency Owner",
        "hs_lead_status": "NEW",
        "lifecyclestage": "lead"
      },
      "createdAt": "2026-04-19T01:27:05.703Z",
      "archived": false
    }
  ],
  "startedAt": "2026-04-19T01:27:05.651Z",
  "completedAt": "2026-04-19T01:27:05.921Z"
}
```

Contact was verified live inside HubSpot CRM dashboard confirming real API connectivity.

---

## Assumptions

- Contact data is seeded mock data (847 Agency Owners, 2,341 Operations Managers, 1,109 Creative Leads)
- Analytics metrics simulate realistic email engagement benchmarks
- HubSpot free developer account used — bulk email sending requires Marketing Hub paid plan
- Content generation falls back to structured mock data if OpenAI quota is exceeded
- Campaign send is logged and simulated — actual email delivery requires HubSpot Marketing Hub

---

## What I'd Build Next

- Real email delivery via HubSpot Marketing Hub or SendGrid
- Slack alerts when open rate drops below a threshold
- Automated A/B subject line testing with statistical significance scoring
- Notion CMS integration to publish blog posts directly
- Webhook listener for real HubSpot engagement events
- Scheduled weekly runs via cron job or GitHub Actions
- Multi-language newsletter generation for global audiences

---

## Running Without API Keys

The app runs in demo mode without API keys:
- Content generation uses structured mock data
- HubSpot calls are simulated with realistic API logs
- All charts, analytics, and campaign history are fully functional

This makes it easy for reviewers to explore the full pipeline without needing credentials.

---

Built by **Rohith Gowda R** · Palona AI Take-Home Assignment · April 2026
