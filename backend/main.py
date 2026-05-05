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
    meal_plan, field_visits, notifications, offline_sync
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
