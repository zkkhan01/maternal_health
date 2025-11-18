from fastapi import FastAPI
from .routers import logs, risk, guidance, dashboard

app = FastAPI(
    title="BloomGuard API",
    description=(
        "BloomGuard - Pregnancy symptom tracker and maternal health platform. "
        "This API exposes endpoints for logging symptoms and vitals, computing risk, "
        "and returning supportive guidance and a basic dashboard view."
    ),
    version="0.1.0",
)

app.include_router(logs.router)
app.include_router(risk.router)
app.include_router(guidance.router)
app.include_router(dashboard.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
