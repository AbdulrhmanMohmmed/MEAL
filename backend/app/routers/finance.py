from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models import Grant, Transaction
from app.auth import get_current_user

router = APIRouter(prefix="/api/finance", tags=["Finance"])


@router.get("/grants")
def list_grants(status: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Grant)
    if status:
        query = query.filter(Grant.status == status)
    grants = query.order_by(Grant.created_at.desc()).all()
    return [{
        "id": g.id, "name": g.name, "donor": g.donor, "amount": g.amount,
        "currency": g.currency, "spent": g.spent, "status": g.status,
        "start_date": str(g.start_date) if g.start_date else None,
        "end_date": str(g.end_date) if g.end_date else None,
        "utilization": round((g.spent / g.amount * 100) if g.amount > 0 else 0, 1),
        "reporting_frequency": g.reporting_frequency
    } for g in grants]


@router.post("/grants")
def create_grant(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    g = Grant(**{k: v for k, v in data.items() if hasattr(Grant, k)})
    db.add(g)
    db.commit()
    db.refresh(g)
    return {"id": g.id, "name": g.name}


@router.get("/transactions")
def list_transactions(
    grant_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Transaction)
    if grant_id:
        query = query.filter(Transaction.grant_id == grant_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    transactions = query.order_by(Transaction.date.desc()).all()
    return [{
        "id": t.id, "grant_id": t.grant_id, "type": t.transaction_type,
        "amount": t.amount, "currency": t.currency, "description": t.description,
        "category": t.category, "date": str(t.date) if t.date else None,
        "reference_number": t.reference_number, "approved_by": t.approved_by
    } for t in transactions]


@router.post("/transactions")
def create_transaction(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = Transaction(**{k: v for k, v in data.items() if hasattr(Transaction, k)})
    db.add(t)
    if data.get("grant_id") and data.get("transaction_type") == "expense":
        grant = db.query(Grant).filter(Grant.id == data["grant_id"]).first()
        if grant:
            grant.spent = (grant.spent or 0) + data.get("amount", 0)
    db.commit()
    return {"message": "Transaction created"}


@router.get("/summary")
def finance_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total_grants = db.query(func.sum(Grant.amount)).scalar() or 0
    total_spent = db.query(func.sum(Grant.spent)).scalar() or 0
    total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.transaction_type == "income").scalar() or 0
    total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.transaction_type == "expense").scalar() or 0
    return {
        "total_grants": total_grants,
        "total_spent": total_spent,
        "total_income": total_income,
        "total_expense": total_expense,
        "burn_rate": round((total_spent / total_grants * 100) if total_grants > 0 else 0, 1)
    }
