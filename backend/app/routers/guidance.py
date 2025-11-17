from fastapi import APIRouter
from ..schemas import GuidanceResponse
from ..risk_engine import engine

router = APIRouter(prefix="/guidance", tags=["guidance"])


@router.get("/{patient_id}", response_model=GuidanceResponse)
async def get_guidance(patient_id: str) -> GuidanceResponse:
    return engine.guidance(patient_id)
