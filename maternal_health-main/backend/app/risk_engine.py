from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from .schemas import (
    SymptomLog,
    VitalLog,
    RiskAssessment,
    GuidanceResponse,
    GuidanceCard,
    PatientSummary,
    DashboardOverview,
)


@dataclass
class PatientState:
    patient_id: str
    symptoms: List[SymptomLog] = field(default_factory=list)
    vitals: List[VitalLog] = field(default_factory=list)
    last_seen: datetime | None = None
    last_gestational_week: int | None = None


class MaternalRiskEngine:
    def __init__(self) -> None:
        self.patients: Dict[str, PatientState] = {}

    def _get_state(self, patient_id: str) -> PatientState:
        if patient_id not in self.patients:
            self.patients[patient_id] = PatientState(patient_id=patient_id)
        return self.patients[patient_id]

    def ingest_symptom(self, log: SymptomLog) -> None:
        state = self._get_state(log.patient_id)
        state.symptoms.append(log)
        state.last_seen = log.timestamp
        state.last_gestational_week = log.gestational_week

    def ingest_vital(self, log: VitalLog) -> None:
        state = self._get_state(log.patient_id)
        state.vitals.append(log)
        state.last_seen = log.timestamp
        state.last_gestational_week = log.gestational_week

    def _windowed_events(
        self,
        state: PatientState,
        horizon: timedelta = timedelta(hours=48),
    ) -> Tuple[List[SymptomLog], List[VitalLog]]:
        if not state.last_seen:
            return [], []
        cutoff = state.last_seen - horizon
        symptoms = [s for s in state.symptoms if s.timestamp >= cutoff]
        vitals = [v for v in state.vitals if v.timestamp >= cutoff]
        return symptoms, vitals

    def _compute_risk_score(self, state: PatientState) -> float:
        symptoms, vitals = self._windowed_events(state)
        if not symptoms and not vitals:
            return 0.1

        score = 0.0

        # Vital based risk
        for v in vitals[-3:]:
            if v.systolic_bp >= 160 or v.diastolic_bp >= 110:
                score += 0.4
            elif v.systolic_bp >= 140 or v.diastolic_bp >= 90:
                score += 0.25

        # Symptom based risk
        concerning_symptoms = {"severe_headache", "vision_changes", "heavy_bleeding", "no_fetal_movement"}
        moderate_symptoms = {"swelling", "dizziness", "shortness_of_breath", "pain"}

        for s in symptoms[-5:]:
            if any(sym in concerning_symptoms for sym in s.symptoms):
                score += 0.3
            if any(sym in moderate_symptoms for sym in s.symptoms):
                score += 0.15
            if s.mood <= 2:
                score += 0.1

        # Normalize roughly into 0 to 1
        return max(0.0, min(1.0, score))

    def _band_for_score(self, score: float) -> str:
        if score < 0.33:
            return "low"
        elif score < 0.66:
            return "medium"
        return "high"

    def _build_explanation(self, state: PatientState, score: float) -> str:
        symptoms, vitals = self._windowed_events(state)
        parts: List[str] = []

        if not symptoms and not vitals:
            return "There is not enough recent information to estimate risk yet. Continue logging symptoms and vitals."

        if vitals:
            latest_bp = vitals[-1]
            if latest_bp.systolic_bp >= 160 or latest_bp.diastolic_bp >= 110:
                parts.append("Your recent blood pressure has been in a higher range that can sometimes be concerning in pregnancy.")
            elif latest_bp.systolic_bp >= 140 or latest_bp.diastolic_bp >= 90:
                parts.append("Your recent blood pressure readings have been somewhat elevated.")

        if symptoms:
            recent = symptoms[-1]
            if "severe_headache" in recent.symptoms or "vision_changes" in recent.symptoms:
                parts.append("You reported headache or vision changes, which can sometimes be warning signs when combined with higher blood pressure.")
            if "heavy_bleeding" in recent.symptoms:
                parts.append("You logged heavier bleeding, which should be discussed with a provider as soon as possible.")
            if "no_fetal_movement" in recent.symptoms:
                parts.append("You noted very little or no fetal movement compared to usual. This can be important to check quickly.")
            if recent.mood <= 2:
                parts.append("Your mood scores have been on the lower side, which matters for your well being.")

        if not parts:
            parts.append("Recent logs look mostly within expected ranges for pregnancy, but the system will keep watching for changes.")

        return " ".join(parts)

    def current_assessment(self, patient_id: str) -> RiskAssessment:
        state = self._get_state(patient_id)
        as_of = state.last_seen or datetime.utcnow()
        score = self._compute_risk_score(state)
        band = self._band_for_score(score)
        explanation = self._build_explanation(state, score)
        return RiskAssessment(
            patient_id=patient_id,
            as_of=as_of,
            gestational_week=state.last_gestational_week,
            risk_band=band,
            risk_score=score,
            explanation=explanation,
        )

    def guidance(self, patient_id: str) -> GuidanceResponse:
        assessment = self.current_assessment(patient_id)
        cards: List[GuidanceCard] = []

        week = assessment.gestational_week or 0

        if assessment.risk_band == "low":
            cards.append(
                GuidanceCard(
                    title="Things seem stable right now",
                    body=(
                        "Based on what you logged, things look mostly within expected ranges. "
                        "Keep paying attention to your body, drink water, and continue your checkins. "
                        "If anything feels suddenly wrong, always trust your instincts and contact your provider."
                    ),
                )
            )
        elif assessment.risk_band == "medium":
            cards.append(
                GuidanceCard(
                    title="Monitor and plan a check in",
                    body=(
                        "Some of your recent symptoms or blood pressure readings are a bit higher than usual. "
                        "Consider writing down what you are noticing and contact your provider to ask if they want an earlier visit or extra checks."
                    ),
                )
            )
            if week >= 28:
                cards.append(
                    GuidanceCard(
                        title="Pay extra attention to fetal movement",
                        body=(
                            "In the third trimester, changes in fetal movement can matter. "
                            "If you notice fewer movements than usual, follow your clinic instructions for counting kicks "
                            "and call if the pattern feels very different."
                        ),
                    )
                )
        else:
            cards.append(
                GuidanceCard(
                    title="High concern items present",
                    body=(
                        "Some of your recent entries suggest symptoms that can be urgent in pregnancy. "
                        "If you have severe pain, heavy bleeding, trouble breathing, chest pain, or a sense that something is very wrong, "
                        "do not wait for the app. Contact emergency services or your hospital now."
                    ),
                )
            )
            cards.append(
                GuidanceCard(
                    title="Call your provider soon",
                    body=(
                        "Even if you are not in immediate danger, this is a good time to call your provider, describe what you logged, "
                        "and ask if they want you to be seen today."
                    ),
                )
            )

        return GuidanceResponse(
            patient_id=patient_id,
            as_of=assessment.as_of,
            gestational_week=assessment.gestational_week,
            risk_band=assessment.risk_band,
            cards=cards,
        )

    def dashboard(self) -> DashboardOverview:
        summaries: List[PatientSummary] = []
        for state in self.patients.values():
            if not state.last_seen:
                continue
            score = self._compute_risk_score(state)
            band = self._band_for_score(score)
            summaries.append(
                PatientSummary(
                    patient_id=state.patient_id,
                    last_seen=state.last_seen,
                    gestational_week=state.last_gestational_week,
                    risk_band=band,
                    risk_score=score,
                )
            )
        generated_at = datetime.utcnow()
        summaries.sort(key=lambda s: s.risk_score, reverse=True)
        return DashboardOverview(generated_at=generated_at, patients=summaries)


engine = MaternalRiskEngine()
