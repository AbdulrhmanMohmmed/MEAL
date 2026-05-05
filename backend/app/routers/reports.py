from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Project, Beneficiary, Indicator, Grant, CashTransfer, Complaint, Distribution
from app.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/project-progress")
def project_progress_report(db: Session = Depends(get_db), user=Depends(get_current_user)):
    projects = db.query(Project).all()
    return [{
        "project": p.name,
        "code": p.code,
        "status": p.status,
        "budget": p.budget,
        "spent": p.spent,
        "budget_utilization": round((p.spent / p.budget * 100) if p.budget > 0 else 0, 1),
        "target_beneficiaries": p.target_beneficiaries,
        "reached_beneficiaries": p.reached_beneficiaries,
        "beneficiary_reach": round((p.reached_beneficiaries / p.target_beneficiaries * 100) if p.target_beneficiaries > 0 else 0, 1),
        "start_date": str(p.start_date) if p.start_date else None,
        "end_date": str(p.end_date) if p.end_date else None
    } for p in projects]


@router.get("/beneficiary-summary")
def beneficiary_summary_report(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.query(Beneficiary).count()
    by_governorate = db.query(Beneficiary.governorate, func.count(Beneficiary.id)).group_by(Beneficiary.governorate).all()
    by_gender = db.query(Beneficiary.gender, func.count(Beneficiary.id)).group_by(Beneficiary.gender).all()
    idp_count = db.query(Beneficiary).filter(Beneficiary.is_idp == True).count()
    disabled = db.query(Beneficiary).filter(Beneficiary.disability == True).count()
    female_headed = db.query(Beneficiary).filter(Beneficiary.female_headed == True).count()
    return {
        "total": total,
        "by_governorate": [{"governorate": r[0], "count": r[1]} for r in by_governorate],
        "by_gender": {r[0]: r[1] for r in by_gender if r[0]},
        "idp_count": idp_count,
        "disabled": disabled,
        "female_headed": female_headed,
        "vulnerability_avg": db.query(func.avg(Beneficiary.vulnerability_score)).scalar() or 0
    }


@router.get("/indicator-tracking")
def indicator_tracking_report(db: Session = Depends(get_db), user=Depends(get_current_user)):
    indicators = db.query(Indicator).all()
    on_track = sum(1 for i in indicators if i.target > 0 and i.current_value >= i.target * 0.8)
    at_risk = sum(1 for i in indicators if i.target > 0 and i.target * 0.5 <= i.current_value < i.target * 0.8)
    off_track = len(indicators) - on_track - at_risk
    return {
        "total_indicators": len(indicators),
        "on_track": on_track,
        "at_risk": at_risk,
        "off_track": off_track,
        "indicators": [{
            "name": i.name, "type": i.indicator_type,
            "baseline": i.baseline, "target": i.target,
            "current": i.current_value,
            "achievement": round((i.current_value / i.target * 100) if i.target > 0 else 0, 1)
        } for i in indicators]
    }


@router.get("/financial-summary")
def financial_summary_report(db: Session = Depends(get_db), user=Depends(get_current_user)):
    grants = db.query(Grant).all()
    total_funding = sum(g.amount for g in grants)
    total_spent = sum(g.spent or 0 for g in grants)
    return {
        "total_funding": total_funding,
        "total_spent": total_spent,
        "remaining": total_funding - total_spent,
        "utilization_rate": round((total_spent / total_funding * 100) if total_funding > 0 else 0, 1),
        "grants": [{
            "name": g.name, "donor": g.donor, "amount": g.amount,
            "spent": g.spent, "status": g.status,
            "utilization": round((g.spent / g.amount * 100) if g.amount > 0 else 0, 1)
        } for g in grants]
    }


@router.get("/distribution-summary")
def distribution_summary_report(db: Session = Depends(get_db), user=Depends(get_current_user)):
    distributions = db.query(Distribution).all()
    total_distributions = len(distributions)
    completed = sum(1 for d in distributions if d.status == "completed")
    total_beneficiaries = sum(d.beneficiaries_count or 0 for d in distributions)
    return {
        "total_distributions": total_distributions,
        "completed": completed,
        "total_beneficiaries_reached": total_beneficiaries,
        "by_location": {}
    }


@router.get("/accountability-summary")
def accountability_summary_report(db: Session = Depends(get_db), user=Depends(get_current_user)):
    complaints = db.query(Complaint).all()
    total = len(complaints)
    resolved = sum(1 for c in complaints if c.status in ["resolved", "closed"])
    return {
        "total_complaints": total,
        "resolved": resolved,
        "pending": total - resolved,
        "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 1),
        "avg_response_days": 3.5
    }
