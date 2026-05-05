from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models import RiskRegister
from app.auth import get_current_user

router = APIRouter(prefix="/api/risks", tags=["Risk Management"])


@router.get("/")
def list_risks(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(RiskRegister)
    if status:
        query = query.filter(RiskRegister.status == status)
    if project_id:
        query = query.filter(RiskRegister.project_id == project_id)
    risks = query.order_by(RiskRegister.created_at.desc()).all()
    return [{
        "id": r.id, "title": r.title, "description": r.description,
        "category": r.category, "likelihood": r.likelihood, "impact": r.impact,
        "risk_level": r.risk_level, "mitigation": r.mitigation,
        "owner": r.owner, "status": r.status, "project_id": r.project_id,
        "risk_score": r.likelihood * r.impact,
        "review_date": str(r.review_date) if r.review_date else None
    } for r in risks]


@router.post("/")
def create_risk(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    likelihood = data.get("likelihood", 3)
    impact = data.get("impact", 3)
    score = likelihood * impact
    data["risk_level"] = "critical" if score >= 20 else ("high" if score >= 12 else ("medium" if score >= 6 else "low"))
    r = RiskRegister(**{k: v for k, v in data.items() if hasattr(RiskRegister, k)})
    db.add(r)
    db.commit()
    db.refresh(r)
    return {"id": r.id, "risk_level": r.risk_level}


@router.put("/{risk_id}")
def update_risk(risk_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    r = db.query(RiskRegister).filter(RiskRegister.id == risk_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Risk not found")
    for key, value in data.items():
        if hasattr(r, key):
            setattr(r, key, value)
    if "likelihood" in data or "impact" in data:
        score = r.likelihood * r.impact
        r.risk_level = "critical" if score >= 20 else ("high" if score >= 12 else ("medium" if score >= 6 else "low"))
    db.commit()
    return {"message": "Updated"}


@router.get("/matrix")
def risk_matrix(db: Session = Depends(get_db), user=Depends(get_current_user)):
    risks = db.query(RiskRegister).filter(RiskRegister.status == "open").all()
    matrix = [[0]*5 for _ in range(5)]
    for r in risks:
        li = min(max(r.likelihood - 1, 0), 4)
        im = min(max(r.impact - 1, 0), 4)
        matrix[li][im] += 1
    return {
        "matrix": matrix,
        "total_open": len(risks),
        "critical": sum(1 for r in risks if r.risk_level == "critical"),
        "high": sum(1 for r in risks if r.risk_level == "high")
    }
