from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models import Indicator, Measurement, Project
from app.auth import get_current_user

router = APIRouter(prefix="/api/monitoring", tags=["Monitoring & Evaluation"])


@router.get("/indicators")
def list_indicators(
    project_id: Optional[int] = None,
    indicator_type: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Indicator)
    if project_id:
        query = query.filter(Indicator.project_id == project_id)
    if indicator_type:
        query = query.filter(Indicator.indicator_type == indicator_type)
    indicators = query.all()
    return [{
        "id": i.id, "name": i.name, "description": i.description,
        "indicator_type": i.indicator_type, "unit": i.unit,
        "baseline": i.baseline, "target": i.target, "current_value": i.current_value,
        "progress": round((i.current_value / i.target * 100) if i.target > 0 else 0, 1),
        "data_source": i.data_source, "frequency": i.frequency,
        "responsible": i.responsible, "sector": i.sector,
        "project_id": i.project_id,
        "status": "on_track" if i.current_value >= i.target * 0.8 else ("at_risk" if i.current_value >= i.target * 0.5 else "off_track")
    } for i in indicators]


@router.post("/indicators")
def create_indicator(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    indicator = Indicator(**{k: v for k, v in data.items() if hasattr(Indicator, k)})
    db.add(indicator)
    db.commit()
    db.refresh(indicator)
    return {"id": indicator.id, "name": indicator.name}


@router.put("/indicators/{indicator_id}")
def update_indicator(indicator_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    indicator = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    for key, value in data.items():
        if hasattr(indicator, key):
            setattr(indicator, key, value)
    db.commit()
    return {"message": "Updated"}


@router.get("/indicators/{indicator_id}/measurements")
def get_measurements(indicator_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    measurements = db.query(Measurement).filter(Measurement.indicator_id == indicator_id).order_by(Measurement.date).all()
    return [{
        "id": m.id, "value": m.value, "date": str(m.date),
        "notes": m.notes, "collected_by": m.collected_by, "verified": m.verified
    } for m in measurements]


@router.post("/measurements")
def add_measurement(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = Measurement(**{k: v for k, v in data.items() if hasattr(Measurement, k)})
    db.add(m)
    indicator = db.query(Indicator).filter(Indicator.id == data.get("indicator_id")).first()
    if indicator:
        indicator.current_value = data.get("value", indicator.current_value)
    db.commit()
    return {"message": "Measurement added"}


@router.get("/iptt")
def indicator_performance_tracking(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Indicator)
    if project_id:
        query = query.filter(Indicator.project_id == project_id)
    indicators = query.all()
    result = []
    for i in indicators:
        measurements = db.query(Measurement).filter(Measurement.indicator_id == i.id).order_by(Measurement.date).all()
        result.append({
            "indicator": {
                "id": i.id, "name": i.name, "type": i.indicator_type,
                "baseline": i.baseline, "target": i.target, "current": i.current_value
            },
            "measurements": [{"date": str(m.date), "value": m.value} for m in measurements],
            "achievement_rate": round((i.current_value / i.target * 100) if i.target > 0 else 0, 1)
        })
    return result


@router.get("/summary")
def monitoring_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.query(Indicator).count()
    on_track = db.query(Indicator).filter(Indicator.current_value >= Indicator.target * 0.8).count()
    at_risk = db.query(Indicator).filter(
        Indicator.current_value >= Indicator.target * 0.5,
        Indicator.current_value < Indicator.target * 0.8
    ).count()
    off_track = total - on_track - at_risk
    return {
        "total_indicators": total,
        "on_track": on_track,
        "at_risk": at_risk,
        "off_track": off_track,
        "overall_achievement": round((on_track / total * 100) if total > 0 else 0, 1)
    }
