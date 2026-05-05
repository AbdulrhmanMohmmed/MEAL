from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.models import (
    Project, Beneficiary, Indicator, Activity, Grant, CashTransfer,
    Complaint, FieldVisit, Distribution, ProjectStatus, BeneficiaryStatus
)
from app.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total_projects = db.query(Project).count()
    active_projects = db.query(Project).filter(Project.status == ProjectStatus.ACTIVE).count()
    total_beneficiaries = db.query(Beneficiary).count()
    active_beneficiaries = db.query(Beneficiary).filter(Beneficiary.status == BeneficiaryStatus.ACTIVE).count()
    total_budget = db.query(func.sum(Project.budget)).scalar() or 0
    total_spent = db.query(func.sum(Project.spent)).scalar() or 0
    total_grants = db.query(Grant).count()
    active_grants = db.query(Grant).filter(Grant.status == "active").count()
    total_indicators = db.query(Indicator).count()
    pending_complaints = db.query(Complaint).filter(Complaint.status.in_(["received", "under_review", "in_progress"])).count()
    upcoming_visits = db.query(FieldVisit).filter(FieldVisit.status == "planned").count()

    indicators_on_track = db.query(Indicator).filter(Indicator.current_value >= Indicator.target * 0.8).count()
    indicator_achievement = round((indicators_on_track / total_indicators * 100) if total_indicators > 0 else 0, 1)

    return {
        "projects": {"total": total_projects, "active": active_projects},
        "beneficiaries": {"total": total_beneficiaries, "active": active_beneficiaries},
        "budget": {"total": total_budget, "spent": total_spent, "utilization": round((total_spent / total_budget * 100) if total_budget > 0 else 0, 1)},
        "grants": {"total": total_grants, "active": active_grants},
        "indicators": {"total": total_indicators, "on_track": indicators_on_track, "achievement": indicator_achievement},
        "complaints": {"pending": pending_complaints},
        "field_visits": {"upcoming": upcoming_visits}
    }


@router.get("/charts/beneficiaries-by-governorate")
def beneficiaries_by_governorate(db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = db.query(Beneficiary.governorate, func.count(Beneficiary.id)).group_by(Beneficiary.governorate).all()
    return [{"governorate": r[0], "count": r[1]} for r in results]


@router.get("/charts/projects-by-sector")
def projects_by_sector(db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = db.query(Project.sector, func.count(Project.id)).group_by(Project.sector).all()
    return [{"sector": r[0], "count": r[1]} for r in results]


@router.get("/charts/budget-by-project")
def budget_by_project(db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = db.query(Project.name, Project.budget, Project.spent).filter(Project.status == ProjectStatus.ACTIVE).all()
    return [{"name": r[0], "budget": r[1], "spent": r[2]} for r in results]


@router.get("/charts/indicator-progress")
def indicator_progress(db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = db.query(Indicator).limit(10).all()
    return [{
        "name": i.name[:40],
        "target": i.target,
        "current": i.current_value,
        "progress": round((i.current_value / i.target * 100) if i.target > 0 else 0, 1)
    } for i in results]


@router.get("/recent-activities")
def recent_activities(db: Session = Depends(get_db), user=Depends(get_current_user)):
    activities = db.query(Activity).order_by(Activity.created_at.desc()).limit(10).all()
    return [{
        "id": a.id,
        "name": a.name,
        "status": a.status,
        "progress": a.progress_percent,
        "project_id": a.project_id
    } for a in activities]
