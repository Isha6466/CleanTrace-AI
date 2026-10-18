# CleanTrace AI

Autonomous multi-agent civic mesh for **street-waste hotspots**.

Citizens report a dirty street with a photo. Three agents hand the case off:

1. **Sentinel** — Gemini vision inspects the photo, scores severity, and labels waste type.
2. **Civic Nudge** — computes a cleanliness index, increments micro-zone strikes, and drafts a Hindi/English RWA notice. After 3 strikes it flags a sanitation surcharge.
3. **Resolver** — compares before/after cleanup photos and marks the incident `RESOLVED` or `REJECTED`.

## Project layout

```
app.py                 Streamlit command desk
agents/
  sentinel.py          Vision inspector
  civic_nudge.py       Strike ledger + bilingual notice
  resolver.py          Before/after verification
  orchestrator.py      Sentinel → Civic Nudge handoff
core/
  config.py            Model name + API key
  client.py            Gemini client
  state.py             Session reports, strikes, logs
ui/                    Tabs, hero banner, theme
```

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste GEMINI_API_KEY
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

## Cloud Run

```bash
./deploy_cloudrun.sh
```

The container listens on port `8080`. Set `GEMINI_API_KEY` as a Cloud Run secret/env var.
