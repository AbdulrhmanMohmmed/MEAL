import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base, SessionLocal
from app.routers import (
    auth, beneficiaries, projects, finance, hr, inventory,
    monitoring, cash, dashboard, data_collection, reports,
    documents, accountability, learning, logframe, risks,
    meal_plan, field_visits, notifications, offline_sync,
    activities, ai_assistant, analytics, assessment_tools,
    audit, compliance, executive, feedback_loop, integrations,
    iptt, kobo_integration, needs_assessment, recommendations,
    remote_monitoring, safeguarding, scheduled_reports,
    sector_indicators, yemen_locations
)
from app.seed import seed_database

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="نظام MEAL - المتابعة والتقييم والمساءلة والتعلم",
    description="نظام متكامل لإدارة MEAL للمنظمات الإنسانية في اليمن",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(beneficiaries.router)
app.include_router(projects.router)
app.include_router(finance.router)
app.include_router(hr.router)
app.include_router(inventory.router)
app.include_router(monitoring.router)
app.include_router(cash.router)
app.include_router(data_collection.router)
app.include_router(reports.router)
app.include_router(documents.router)
app.include_router(accountability.router)
app.include_router(learning.router)
app.include_router(logframe.router)
app.include_router(risks.router)
app.include_router(meal_plan.router)
app.include_router(field_visits.router)
app.include_router(notifications.router)
app.include_router(offline_sync.router)
app.include_router(activities.router)
app.include_router(ai_assistant.router)
app.include_router(analytics.router)
app.include_router(assessment_tools.router)
app.include_router(audit.router)
app.include_router(compliance.router)
app.include_router(executive.router)
app.include_router(feedback_loop.router)
app.include_router(integrations.router)
app.include_router(iptt.router)
app.include_router(kobo_integration.router)
app.include_router(needs_assessment.router)
app.include_router(recommendations.router)
app.include_router(remote_monitoring.router)
app.include_router(safeguarding.router)
app.include_router(scheduled_reports.router)
app.include_router(sector_indicators.router)
app.include_router(yemen_locations.router)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend_dist")
if os.path.exists(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        file_path = os.path.join(FRONTEND_DIR, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
else:
    @app.get("/")
    def root():
        return {"message": "MEAL System API - Yemen", "version": "2.0.0", "docs": "/docs"}


@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
