from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Warehouse, InventoryItem, Distribution
from app.auth import get_current_user

router = APIRouter(prefix="/api/inventory", tags=["Inventory & Supply Chain"])


@router.get("/warehouses")
def list_warehouses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    warehouses = db.query(Warehouse).all()
    result = []
    for w in warehouses:
        items_count = db.query(InventoryItem).filter(InventoryItem.warehouse_id == w.id).count()
        low_stock = db.query(InventoryItem).filter(
            InventoryItem.warehouse_id == w.id,
            InventoryItem.quantity <= InventoryItem.min_stock
        ).count()
        result.append({
            "id": w.id, "name": w.name, "location": w.location,
            "governorate": w.governorate, "capacity": w.capacity,
            "manager": w.manager, "is_active": w.is_active,
            "items_count": items_count, "low_stock_alerts": low_stock
        })
    return result


@router.get("/items")
def list_items(warehouse_id: Optional[int] = None, category: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(InventoryItem)
    if warehouse_id:
        query = query.filter(InventoryItem.warehouse_id == warehouse_id)
    if category:
        query = query.filter(InventoryItem.category == category)
    items = query.all()
    return [{
        "id": i.id, "name": i.name, "category": i.category,
        "quantity": i.quantity, "unit": i.unit, "min_stock": i.min_stock,
        "warehouse_id": i.warehouse_id,
        "expiry_date": str(i.expiry_date) if i.expiry_date else None,
        "is_low_stock": i.quantity <= i.min_stock
    } for i in items]


@router.post("/items")
def create_item(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = InventoryItem(**{k: v for k, v in data.items() if hasattr(InventoryItem, k)})
    db.add(item)
    db.commit()
    return {"message": "Item added"}


@router.get("/distributions")
def list_distributions(status: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Distribution)
    if status:
        query = query.filter(Distribution.status == status)
    distributions = query.order_by(Distribution.date.desc()).all()
    return [{
        "id": d.id, "item_name": d.item_name, "quantity": d.quantity,
        "beneficiaries_count": d.beneficiaries_count, "location": d.location,
        "date": str(d.date) if d.date else None, "status": d.status,
        "distributed_by": d.distributed_by, "notes": d.notes
    } for d in distributions]


@router.post("/distributions")
def create_distribution(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    d = Distribution(**{k: v for k, v in data.items() if hasattr(Distribution, k)})
    db.add(d)
    db.commit()
    return {"message": "Distribution created"}


@router.get("/alerts")
def stock_alerts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    low_stock = db.query(InventoryItem).filter(InventoryItem.quantity <= InventoryItem.min_stock).all()
    return [{
        "id": i.id, "name": i.name, "quantity": i.quantity,
        "min_stock": i.min_stock, "warehouse_id": i.warehouse_id,
        "alert_type": "critical" if i.quantity == 0 else "low"
    } for i in low_stock]
