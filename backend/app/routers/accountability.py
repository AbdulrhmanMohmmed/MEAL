from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import Complaint
from app.auth import get_current_user

router = APIRouter(prefix="/api/accountability", tags=["Accountability & CFM"])


@router.get("/complaints")
def list_complaints(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Complaint)
    if status:
        query = query.filter(Complaint.status == status)
    if priority:
        query = query.filter(Complaint.priority == priority)
    if category:
        query = query.filter(Complaint.category == category)
    complaints = query.order_by(Complaint.created_at.desc()).all()
    return [{
        "id": c.id, "reference_number": c.reference_number, "channel": c.channel,
        "category": c.category, "priority": c.priority, "status": c.status,
        "description": c.description, "complainant_name": c.complainant_name if not c.is_anonymous else "Anonymous",
        "location": c.location, "project_id": c.project_id,
        "assigned_to": c.assigned_to, "is_sensitive": c.is_sensitive,
        "created_at": str(c.created_at) if c.created_at else None,
        "response_date": str(c.response_date) if c.response_date else None
    } for c in complaints]


@router.post("/complaints")
def create_complaint(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    count = db.query(Complaint).count()
    data["reference_number"] = f"CFM-{datetime.now().year}-{count + 1:04d}"
    c = Complaint(**{k: v for k, v in data.items() if hasattr(Complaint, k)})
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "reference_number": c.reference_number}


@router.put("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    for key, value in data.items():
        if hasattr(c, key):
            setattr(c, key, value)
    if data.get("status") in ["resolved", "closed"]:
        c.closed_at = datetime.utcnow()
    db.commit()
    return {"message": "Updated"}


@router.put("/complaints/{complaint_id}/resolve")
def resolve_complaint(complaint_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    c.status = "resolved"
    c.resolution = data.get("resolution", "")
    c.response_date = datetime.utcnow()
    c.closed_at = datetime.utcnow()
    db.commit()
    return {"message": "Complaint resolved"}


@router.get("/summary")
def accountability_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.query(Complaint).count()
    by_status = db.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    by_channel = db.query(Complaint.channel, func.count(Complaint.id)).group_by(Complaint.channel).all()
    by_category = db.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"])).count()
    return {
        "total": total,
        "resolved": resolved,
        "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 1),
        "by_status": {r[0]: r[1] for r in by_status},
        "by_channel": {r[0]: r[1] for r in by_channel},
        "by_category": {r[0]: r[1] for r in by_category}
    }
