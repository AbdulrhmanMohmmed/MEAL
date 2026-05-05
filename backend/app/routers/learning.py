from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models import LessonLearned
from app.auth import get_current_user

router = APIRouter(prefix="/api/learning", tags=["Learning"])


@router.get("/lessons")
def list_lessons(
    category: Optional[str] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(LessonLearned)
    if category:
        query = query.filter(LessonLearned.category == category)
    if project_id:
        query = query.filter(LessonLearned.project_id == project_id)
    lessons = query.order_by(LessonLearned.date.desc()).all()
    return [{
        "id": l.id, "title": l.title, "description": l.description,
        "category": l.category, "project_id": l.project_id,
        "source": l.source, "recommendations": l.recommendations,
        "shared_with": l.shared_with, "date": str(l.date) if l.date else None
    } for l in lessons]


@router.post("/lessons")
def create_lesson(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    l = LessonLearned(**{k: v for k, v in data.items() if hasattr(LessonLearned, k)})
    db.add(l)
    db.commit()
    db.refresh(l)
    return {"id": l.id, "title": l.title}


@router.put("/lessons/{lesson_id}")
def update_lesson(lesson_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    l = db.query(LessonLearned).filter(LessonLearned.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for key, value in data.items():
        if hasattr(l, key):
            setattr(l, key, value)
    db.commit()
    return {"message": "Updated"}


@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    l = db.query(LessonLearned).filter(LessonLearned.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(l)
    db.commit()
    return {"message": "Deleted"}


@router.get("/summary")
def learning_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.query(LessonLearned).count()
    by_category = db.query(LessonLearned.category, func.count(LessonLearned.id)).group_by(LessonLearned.category).all()
    return {
        "total": total,
        "by_category": {r[0]: r[1] for r in by_category if r[0]}
    }
