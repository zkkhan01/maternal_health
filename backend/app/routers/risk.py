from fastapi import APIRouter
from ..schemas import RiskAssessment
from ..risk_engine import engine

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/{patient_id}", response_model=RiskAssessment)
async def get_risk(patient_id: str) -> RiskAssessment:
    return engine.current_assessment(patient_id)
