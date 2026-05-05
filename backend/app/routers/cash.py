from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models import CashTransfer
from app.auth import get_current_user

router = APIRouter(prefix="/api/cash", tags=["Cash & Voucher Assistance"])


@router.get("/transfers")
def list_transfers(
    status: Optional[str] = None,
    method: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(CashTransfer)
    if status:
        query = query.filter(CashTransfer.status == status)
    if method:
        query = query.filter(CashTransfer.method == method)
    transfers = query.order_by(CashTransfer.created_at.desc()).all()
    return [{
        "id": t.id, "beneficiary_id": t.beneficiary_id, "project_id": t.project_id,
        "amount": t.amount, "currency": t.currency, "method": t.method,
        "status": t.status, "transfer_date": str(t.transfer_date) if t.transfer_date else None,
        "reference_number": t.reference_number, "agent": t.agent,
        "verified": t.verified, "notes": t.notes
    } for t in transfers]


@router.post("/transfers")
def create_transfer(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = CashTransfer(**{k: v for k, v in data.items() if hasattr(CashTransfer, k)})
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"id": t.id, "reference_number": t.reference_number}


@router.put("/transfers/{transfer_id}/verify")
def verify_transfer(transfer_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = db.query(CashTransfer).filter(CashTransfer.id == transfer_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transfer not found")
    t.verified = True
    t.status = "received"
    db.commit()
    return {"message": "Transfer verified"}


@router.get("/summary")
def cash_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total_amount = db.query(func.sum(CashTransfer.amount)).scalar() or 0
    total_transfers = db.query(CashTransfer).count()
    disbursed = db.query(func.sum(CashTransfer.amount)).filter(CashTransfer.status.in_(["disbursed", "received"])).scalar() or 0
    by_method = db.query(CashTransfer.method, func.count(CashTransfer.id), func.sum(CashTransfer.amount)).group_by(CashTransfer.method).all()
    return {
        "total_amount": total_amount,
        "total_transfers": total_transfers,
        "disbursed": disbursed,
        "pending": total_amount - disbursed,
        "by_method": [{"method": r[0], "count": r[1], "amount": r[2] or 0} for r in by_method]
    }
