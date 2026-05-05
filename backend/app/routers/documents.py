from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Document
from app.auth import get_current_user

router = APIRouter(prefix="/api/documents", tags=["Document Archive"])


@router.get("/")
def list_documents(
    category: Optional[str] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Document)
    if category:
        query = query.filter(Document.category == category)
    if project_id:
        query = query.filter(Document.project_id == project_id)
    docs = query.order_by(Document.created_at.desc()).all()
    return [{
        "id": d.id, "title": d.title, "category": d.category,
        "file_path": d.file_path, "file_size": d.file_size,
        "project_id": d.project_id, "uploaded_by": d.uploaded_by,
        "tags": d.tags.split(",") if d.tags else [],
        "description": d.description,
        "created_at": str(d.created_at) if d.created_at else None
    } for d in docs]


@router.post("/")
def create_document(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if isinstance(data.get("tags"), list):
        data["tags"] = ",".join(data["tags"])
    d = Document(**{k: v for k, v in data.items() if hasattr(Document, k)})
    d.uploaded_by = user.full_name
    db.add(d)
    db.commit()
    db.refresh(d)
    return {"id": d.id, "title": d.title}


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    d = db.query(Document).filter(Document.id == doc_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(d)
    db.commit()
    return {"message": "Deleted"}
