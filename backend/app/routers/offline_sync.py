from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import OfflineQueue, FormSubmission, Beneficiary
from app.auth import get_current_user

router = APIRouter(prefix="/api/offline", tags=["Offline Sync"])


@router.post("/sync")
def sync_offline_data(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = data.get("items", [])
    synced_count = 0
    errors = []

    for item in items:
        try:
            if item.get("type") == "form_submission":
                submission = FormSubmission(
                    form_id=item["data"]["form_id"],
                    data=item["data"].get("responses", {}),
                    submitted_by=user.full_name,
                    status="submitted",
                    location_lat=item["data"].get("latitude"),
                    location_lng=item["data"].get("longitude"),
                    synced=True
                )
                db.add(submission)
            elif item.get("type") == "beneficiary":
                ben_data = item["data"]
                b = Beneficiary(**{k: v for k, v in ben_data.items() if hasattr(Beneficiary, k)})
                db.add(b)

            queue_entry = OfflineQueue(
                device_id=data.get("device_id", "unknown"),
                action=item.get("action", "create"),
                resource_type=item.get("type"),
                data=item.get("data"),
                synced=True,
                synced_at=datetime.utcnow()
            )
            db.add(queue_entry)
            synced_count += 1
        except Exception as e:
            errors.append({"item": item.get("id"), "error": str(e)})

    db.commit()
    return {
        "synced": synced_count,
        "errors": errors,
        "total": len(items),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/status")
def sync_status(device_id: str = "all", db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(OfflineQueue)
    if device_id != "all":
        query = query.filter(OfflineQueue.device_id == device_id)
    total = query.count()
    synced = query.filter(OfflineQueue.synced == True).count()
    pending = total - synced
    return {
        "total": total,
        "synced": synced,
        "pending": pending,
        "last_sync": None
    }


@router.get("/pending")
def get_pending(device_id: str = "all", db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(OfflineQueue).filter(OfflineQueue.synced == False)
    if device_id != "all":
        query = query.filter(OfflineQueue.device_id == device_id)
    items = query.all()
    return [{
        "id": i.id, "action": i.action, "resource_type": i.resource_type,
        "data": i.data, "created_at": str(i.created_at)
    } for i in items]
