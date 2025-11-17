from __future__ import annotations

import pathway as pw


class SymptomSchema(pw.Schema):
    patient_id: pw.Column[str]
    timestamp: pw.Column[pw.DateTime]
    gestational_week: pw.Column[int]
    symptoms: pw.Column[str]
    mood: pw.Column[int]
    notes: pw.Column[str]


class VitalSchema(pw.Schema):
    patient_id: pw.Column[str]
    timestamp: pw.Column[pw.DateTime]
    gestational_week: pw.Column[int]
    systolic_bp: pw.Column[int]
    diastolic_bp: pw.Column[int]
    heart_rate: pw.Column[int]
    weight_kg: pw.Column[float]


def build_demo_pipeline() -> tuple[pw.Table, pw.Table]:
    # Demo streaming pipeline that reads JSONL files from folders.
    symptoms = pw.io.jsonlines.read(
        "data/stream/symptoms/",
        schema=SymptomSchema,
        mode="streaming",
    )
    vitals = pw.io.jsonlines.read(
        "data/stream/vitals/",
        schema=VitalSchema,
        mode="streaming",
    )
    return symptoms, vitals


def run():
    symptoms, vitals = build_demo_pipeline()
    combined = symptoms.join_left(
        vitals,
        pw.left.patient_id == pw.right.patient_id,
    )
    _ = combined
    pw.run()
