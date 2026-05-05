from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Project, Activity, Indicator
from app.auth import get_current_user

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/")
def list_projects(
    skip: int = 0, limit: int = 50,
    status: Optional[str] = None,
    sector: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    if sector:
        query = query.filter(Project.sector == sector)
    total = query.count()
    items = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "items": [_serialize(p) for p in items]}


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    result = _serialize(p)
    result["activities"] = [{
        "id": a.id, "name": a.name, "status": a.status,
        "progress_percent": a.progress_percent
    } for a in p.activities]
    result["indicators"] = [{
        "id": i.id, "name": i.name, "target": i.target,
        "current_value": i.current_value, "indicator_type": i.indicator_type
    } for i in p.indicators]
    return result


@router.post("/")
def create_project(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = Project(**{k: v for k, v in data.items() if hasattr(Project, k)})
    db.add(p)
    db.commit()
    db.refresh(p)
    return _serialize(p)


@router.put("/{project_id}")
def update_project(project_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in data.items():
        if hasattr(p, key):
            setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return _serialize(p)


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(p)
    db.commit()
    return {"message": "Deleted successfully"}


def _serialize(p):
    return {
        "id": p.id, "name": p.name, "code": p.code, "description": p.description,
        "sector": p.sector, "status": p.status,
        "start_date": str(p.start_date) if p.start_date else None,
        "end_date": str(p.end_date) if p.end_date else None,
        "budget": p.budget, "spent": p.spent, "currency": p.currency,
        "governorate": p.governorate, "donor": p.donor,
        "target_beneficiaries": p.target_beneficiaries,
        "reached_beneficiaries": p.reached_beneficiaries,
        "progress": round((p.spent / p.budget * 100) if p.budget > 0 else 0, 1),
        "created_at": str(p.created_at) if p.created_at else None
    }
