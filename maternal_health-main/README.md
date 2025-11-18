# BloomGuard - Pregnancy Symptom Tracker and Maternal Health Platform

BloomGuard is a maternal health prototype that helps expectant mothers log symptoms,
track vital changes, and receive gentle, personalized guidance throughout pregnancy.

It is designed for a hackathon style demo and uses a Pathway friendly structure together
with a FastAPI backend.

## What this project does

- Lets expectant mothers log daily pregnancy symptoms and moods.
- Stores vitals such as blood pressure, heart rate, and weight.
- Computes a simple maternal risk level from recent symptoms and vitals.
- Returns clear explanations that describe why risk is elevated.
- Provides supportive guidance cards instead of generic internet advice.
- Exposes a basic dashboard overview for clinicians or care teams.

This is a proof of concept and is not a medical device or diagnostic tool.

## Repository layout

- `backend/app/main.py` - FastAPI application entrypoint.
- `backend/app/schemas.py` - Pydantic models for requests and responses.
- `backend/app/risk_engine.py` - in memory maternal risk computation and guidance logic.
- `backend/app/pathway_pipeline.py` - Pathway streaming demo over symptom and vital logs.
- `backend/app/routers/logs.py` - ingestion endpoints for symptoms and vitals.
- `backend/app/routers/risk.py` - risk and explanation endpoint.
- `backend/app/routers/guidance.py` - guidance endpoint returning supportive cards.
- `backend/app/routers/dashboard.py` - dashboard overview endpoint.
- `docs/architecture.md` - Mermaid diagram that GitHub can render.
- `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.gitignore` - setup and deployment.
- `backend/tests/test_health.py` - minimal test for health endpoint.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn backend.app.main:app --reload --port 8020
```

Then open `http://localhost:8020/docs` to explore the API.

## Demo flow suggestion

1. Create a demo patient and log a few days of normal symptoms and vitals.
2. Call the risk endpoint to show a low or medium risk band and calm explanation.
3. Log higher blood pressure and concerning symptoms such as headache, visual changes,
   swelling, or reduced fetal movement.
4. Call the risk endpoint again and point out the higher risk and new explanation.
5. Call the guidance endpoint to show trimester aware, supportive guidance cards.
6. Show the dashboard endpoint listing patients and their relative risk.

## Safety notes

- Use only synthetic or anonymized data.
- This project does not replace professional medical judgment.
- Risk scores and guidance here are for demonstration only.
