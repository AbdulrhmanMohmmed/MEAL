from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import LogFrame
from app.auth import get_current_user

router = APIRouter(prefix="/api/logframe", tags=["Logical Framework"])


@router.get("/")
def list_logframes(project_id: Optional[int] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(LogFrame)
    if project_id:
        query = query.filter(LogFrame.project_id == project_id)
    items = query.order_by(LogFrame.level, LogFrame.code).all()
    return [{
        "id": lf.id, "project_id": lf.project_id, "level": lf.level,
        "code": lf.code, "description": lf.description,
        "indicators": lf.indicators, "means_of_verification": lf.means_of_verification,
        "assumptions": lf.assumptions, "parent_id": lf.parent_id
    } for lf in items]


@router.post("/")
def create_logframe(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lf = LogFrame(**{k: v for k, v in data.items() if hasattr(LogFrame, k)})
    db.add(lf)
    db.commit()
    db.refresh(lf)
    return {"id": lf.id}


@router.put("/{logframe_id}")
def update_logframe(logframe_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lf = db.query(LogFrame).filter(LogFrame.id == logframe_id).first()
    if not lf:
        raise HTTPException(status_code=404, detail="LogFrame not found")
    for key, value in data.items():
        if hasattr(lf, key):
            setattr(lf, key, value)
    db.commit()
    return {"message": "Updated"}


@router.delete("/{logframe_id}")
def delete_logframe(logframe_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lf = db.query(LogFrame).filter(LogFrame.id == logframe_id).first()
    if not lf:
        raise HTTPException(status_code=404, detail="LogFrame not found")
    db.delete(lf)
    db.commit()
    return {"message": "Deleted"}
