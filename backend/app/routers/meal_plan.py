from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import MEALPlan
from app.auth import get_current_user

router = APIRouter(prefix="/api/meal-plan", tags=["MEAL Plan"])


@router.get("/")
def list_plans(project_id: Optional[int] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(MEALPlan)
    if project_id:
        query = query.filter(MEALPlan.project_id == project_id)
    plans = query.order_by(MEALPlan.created_at.desc()).all()
    return [{
        "id": p.id, "project_id": p.project_id, "title": p.title,
        "objectives": p.objectives, "data_collection_methods": p.data_collection_methods,
        "frequency": p.frequency, "responsible_staff": p.responsible_staff,
        "budget": p.budget, "status": p.status
    } for p in plans]


@router.post("/")
def create_plan(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = MEALPlan(**{k: v for k, v in data.items() if hasattr(MEALPlan, k)})
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "title": p.title}


@router.put("/{plan_id}")
def update_plan(plan_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(MEALPlan).filter(MEALPlan.id == plan_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Plan not found")
    for key, value in data.items():
        if hasattr(p, key):
            setattr(p, key, value)
    db.commit()
    return {"message": "Updated"}


@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(MEALPlan).filter(MEALPlan.id == plan_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(p)
    db.commit()
    return {"message": "Deleted"}
