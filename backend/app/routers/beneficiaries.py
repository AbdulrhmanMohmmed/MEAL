from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.database import get_db
from app.models import Beneficiary
from app.auth import get_current_user

router = APIRouter(prefix="/api/beneficiaries", tags=["Beneficiaries"])


@router.get("/")
def list_beneficiaries(
    skip: int = 0, limit: int = 50,
    search: Optional[str] = None,
    governorate: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Beneficiary)
    if search:
        query = query.filter(or_(
            Beneficiary.full_name.contains(search),
            Beneficiary.national_id.contains(search),
            Beneficiary.phone.contains(search)
        ))
    if governorate:
        query = query.filter(Beneficiary.governorate == governorate)
    if status:
        query = query.filter(Beneficiary.status == status)
    total = query.count()
    items = query.order_by(Beneficiary.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "items": [_serialize(b) for b in items]}


@router.get("/{beneficiary_id}")
def get_beneficiary(beneficiary_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    b = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return _serialize(b)


@router.post("/")
def create_beneficiary(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if data.get("national_id"):
        existing = db.query(Beneficiary).filter(Beneficiary.national_id == data["national_id"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Beneficiary with this national ID already exists (duplicate)")
    b = Beneficiary(**{k: v for k, v in data.items() if hasattr(Beneficiary, k)})
    db.add(b)
    db.commit()
    db.refresh(b)
    return _serialize(b)


@router.put("/{beneficiary_id}")
def update_beneficiary(beneficiary_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    b = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    for key, value in data.items():
        if hasattr(b, key):
            setattr(b, key, value)
    db.commit()
    db.refresh(b)
    return _serialize(b)


@router.delete("/{beneficiary_id}")
def delete_beneficiary(beneficiary_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    b = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    db.delete(b)
    db.commit()
    return {"message": "Deleted successfully"}


@router.get("/check-duplicate/{national_id}")
def check_duplicate(national_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(Beneficiary).filter(Beneficiary.national_id == national_id).first()
    return {"exists": existing is not None, "beneficiary": _serialize(existing) if existing else None}


def _serialize(b):
    if not b:
        return None
    return {
        "id": b.id, "national_id": b.national_id, "full_name": b.full_name,
        "gender": b.gender, "date_of_birth": str(b.date_of_birth) if b.date_of_birth else None,
        "phone": b.phone, "governorate": b.governorate, "district": b.district,
        "village": b.village, "household_size": b.household_size,
        "vulnerability_score": b.vulnerability_score, "status": b.status,
        "registration_date": str(b.registration_date) if b.registration_date else None,
        "is_idp": b.is_idp, "disability": b.disability, "female_headed": b.female_headed,
        "latitude": b.latitude, "longitude": b.longitude, "notes": b.notes,
        "created_at": str(b.created_at) if b.created_at else None
    }
