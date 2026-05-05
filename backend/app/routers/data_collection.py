from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import DataForm, FormSubmission
from app.auth import get_current_user

router = APIRouter(prefix="/api/data-collection", tags=["Data Collection"])


@router.get("/forms")
def list_forms(status: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(DataForm)
    if status:
        query = query.filter(DataForm.status == status)
    forms = query.order_by(DataForm.created_at.desc()).all()
    return [{
        "id": f.id, "title": f.title, "description": f.description,
        "status": f.status, "project_id": f.project_id,
        "fields_count": len(f.fields) if f.fields else 0,
        "submissions_count": len(f.submissions) if f.submissions else 0,
        "created_by": f.created_by,
        "created_at": str(f.created_at) if f.created_at else None
    } for f in forms]


@router.get("/forms/{form_id}")
def get_form(form_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    f = db.query(DataForm).filter(DataForm.id == form_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Form not found")
    return {
        "id": f.id, "title": f.title, "description": f.description,
        "status": f.status, "fields": f.fields, "project_id": f.project_id,
        "created_by": f.created_by,
        "submissions": [{
            "id": s.id, "data": s.data, "status": s.status,
            "submitted_by": s.submitted_by,
            "submitted_at": str(s.submitted_at) if s.submitted_at else None,
            "location": {"lat": s.location_lat, "lng": s.location_lng} if s.location_lat else None
        } for s in f.submissions]
    }


@router.post("/forms")
def create_form(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    f = DataForm(
        title=data["title"],
        description=data.get("description"),
        fields=data.get("fields", []),
        project_id=data.get("project_id"),
        created_by=user.full_name,
        status=data.get("status", "draft")
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return {"id": f.id, "title": f.title}


@router.put("/forms/{form_id}")
def update_form(form_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    f = db.query(DataForm).filter(DataForm.id == form_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Form not found")
    for key, value in data.items():
        if hasattr(f, key):
            setattr(f, key, value)
    db.commit()
    return {"message": "Form updated"}


@router.post("/submissions")
def submit_form(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = FormSubmission(
        form_id=data["form_id"],
        data=data.get("data", {}),
        submitted_by=user.full_name,
        status="submitted",
        location_lat=data.get("latitude"),
        location_lng=data.get("longitude"),
        synced=data.get("synced", True)
    )
    db.add(s)
    db.commit()
    return {"message": "Submission recorded", "id": s.id}


@router.get("/submissions")
def list_submissions(form_id: Optional[int] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(FormSubmission)
    if form_id:
        query = query.filter(FormSubmission.form_id == form_id)
    submissions = query.order_by(FormSubmission.submitted_at.desc()).all()
    return [{
        "id": s.id, "form_id": s.form_id, "data": s.data,
        "status": s.status, "submitted_by": s.submitted_by,
        "submitted_at": str(s.submitted_at) if s.submitted_at else None,
        "synced": s.synced
    } for s in submissions]
