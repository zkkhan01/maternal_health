from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel


RiskBand = Literal["low", "medium", "high"]


class SymptomLog(BaseModel):
    patient_id: str
    timestamp: datetime
    gestational_week: int
    symptoms: List[str]
    mood: int  # 1 to 5
    notes: Optional[str] = None


class VitalLog(BaseModel):
    patient_id: str
    timestamp: datetime
    gestational_week: int
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int
    weight_kg: float


class RiskAssessment(BaseModel):
    patient_id: str
    as_of: datetime
    gestational_week: Optional[int]
    risk_band: RiskBand
    risk_score: float
    explanation: str


class GuidanceCard(BaseModel):
    title: str
    body: str


class GuidanceResponse(BaseModel):
    patient_id: str
    as_of: datetime
    gestational_week: Optional[int]
    risk_band: RiskBand
    cards: List[GuidanceCard]


class PatientSummary(BaseModel):
    patient_id: str
    last_seen: datetime
    gestational_week: Optional[int]
    risk_band: RiskBand
    risk_score: float


class DashboardOverview(BaseModel):
    generated_at: datetime
    patients: List[PatientSummary]
