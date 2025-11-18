from fastapi import APIRouter
from ..schemas import SymptomLog, VitalLog
from ..risk_engine import engine

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/symptoms")
async def log_symptom(payload: SymptomLog):
    engine.ingest_symptom(payload)
    return {"status": "ok"}


@router.post("/vitals")
async def log_vitals(payload: VitalLog):
    engine.ingest_vital(payload)
    return {"status": "ok"}
