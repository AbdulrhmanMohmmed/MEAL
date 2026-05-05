from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import FieldVisit
from app.auth import get_current_user

router = APIRouter(prefix="/api/field-visits", tags=["Field Visits"])


@router.get("/")
def list_visits(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(FieldVisit)
    if status:
        query = query.filter(FieldVisit.status == status)
    if project_id:
        query = query.filter(FieldVisit.project_id == project_id)
    visits = query.order_by(FieldVisit.visit_date.desc()).all()
    return [{
        "id": v.id, "project_id": v.project_id,
        "visit_date": str(v.visit_date) if v.visit_date else None,
        "location": v.location, "purpose": v.purpose,
        "findings": v.findings, "recommendations": v.recommendations,
        "follow_up_actions": v.follow_up_actions,
        "visited_by": v.visited_by, "status": v.status,
        "photos_count": v.photos_count
    } for v in visits]


@router.post("/")
def create_visit(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    v = FieldVisit(**{k: v for k, v in data.items() if hasattr(FieldVisit, k)})
    db.add(v)
    db.commit()
    db.refresh(v)
    return {"id": v.id}


@router.put("/{visit_id}")
def update_visit(visit_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    v = db.query(FieldVisit).filter(FieldVisit.id == visit_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Visit not found")
    for key, value in data.items():
        if hasattr(v, key):
            setattr(v, key, value)
    db.commit()
    return {"message": "Updated"}


@router.put("/{visit_id}/complete")
def complete_visit(visit_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    v = db.query(FieldVisit).filter(FieldVisit.id == visit_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Visit not found")
    v.status = "completed"
    v.findings = data.get("findings", v.findings)
    v.recommendations = data.get("recommendations", v.recommendations)
    v.follow_up_actions = data.get("follow_up_actions", v.follow_up_actions)
    db.commit()
    return {"message": "Visit completed"}
