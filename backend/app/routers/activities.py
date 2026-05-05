from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.database import get_db
from app.models import Activity, User
from app.auth import get_current_user

router = APIRouter(prefix="/api/activities", tags=["تتبع الأنشطة"])


@router.get("/")
def list_activities(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Activity)
    if project_id:
        query = query.filter(Activity.project_id == project_id)
    return query.order_by(Activity.id).all()


@router.post("/")
def create_activity(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity = Activity(**{k: v for k, v in data.items() if hasattr(Activity, k)})
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.put("/{activity_id}")
def update_activity(
    activity_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="النشاط غير موجود")
    for k, v in data.items():
        if hasattr(activity, k):
            setattr(activity, k, v)
    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="النشاط غير موجود")
    db.delete(activity)
    db.commit()
    return {"detail": "تم حذف النشاط"}


@router.get("/gantt/{project_id}")
def gantt_data(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activities = db.query(Activity).filter(
        Activity.project_id == project_id
    ).order_by(Activity.id).all()

    gantt_items = []
    for a in activities:
        item = {
            "id": a.id,
            "name": a.name,
            "planned_start": str(a.planned_start) if a.planned_start else None,
            "planned_end": str(a.planned_end) if a.planned_end else None,
            "actual_start": str(a.actual_start) if a.actual_start else None,
            "actual_end": str(a.actual_end) if a.actual_end else None,
            "progress": a.progress_percent,
            "status": a.status,
            "responsible": a.responsible_person,
            "variance_days": None,
        }
        if a.planned_end and a.actual_end:
            item["variance_days"] = (a.actual_end - a.planned_end).days
        elif a.planned_end and not a.actual_end and a.progress_percent < 100:
            item["variance_days"] = (date.today() - a.planned_end).days if date.today() > a.planned_end else 0
        gantt_items.append(item)

    total = len(gantt_items)
    avg_progress = round(sum(g["progress"] or 0 for g in gantt_items) / total, 1) if total else 0
    on_track = len([g for g in gantt_items if (g["variance_days"] or 0) <= 0])
    delayed = len([g for g in gantt_items if (g["variance_days"] or 0) > 0])

    return {
        "activities": gantt_items,
        "summary": {
            "total": total,
            "avg_progress": avg_progress,
            "on_track": on_track,
            "delayed": delayed,
        },
    }
