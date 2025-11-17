from fastapi import APIRouter
from ..schemas import DashboardOverview
from ..risk_engine import engine

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
async def overview() -> DashboardOverview:
    return engine.dashboard()
