from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Employee, LeaveRequest
from app.auth import get_current_user

router = APIRouter(prefix="/api/hr", tags=["Human Resources"])


@router.get("/employees")
def list_employees(
    department: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department == department)
    if status:
        query = query.filter(Employee.status == status)
    employees = query.order_by(Employee.full_name).all()
    return [{
        "id": e.id, "employee_id": e.employee_id, "full_name": e.full_name,
        "email": e.email, "phone": e.phone, "department": e.department,
        "position": e.position, "status": e.status, "location": e.location,
        "join_date": str(e.join_date) if e.join_date else None,
        "contract_type": e.contract_type, "supervisor": e.supervisor
    } for e in employees]


@router.post("/employees")
def create_employee(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    e = Employee(**{k: v for k, v in data.items() if hasattr(Employee, k)})
    db.add(e)
    db.commit()
    db.refresh(e)
    return {"id": e.id, "full_name": e.full_name}


@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    e = db.query(Employee).filter(Employee.id == employee_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in data.items():
        if hasattr(e, key):
            setattr(e, key, value)
    db.commit()
    return {"message": "Updated"}


@router.get("/leaves")
def list_leaves(status: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(LeaveRequest)
    if status:
        query = query.filter(LeaveRequest.status == status)
    leaves = query.order_by(LeaveRequest.created_at.desc()).all()
    return [{
        "id": l.id, "employee_id": l.employee_id, "leave_type": l.leave_type,
        "start_date": str(l.start_date), "end_date": str(l.end_date),
        "reason": l.reason, "status": l.status, "approved_by": l.approved_by
    } for l in leaves]


@router.post("/leaves")
def create_leave(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    l = LeaveRequest(**{k: v for k, v in data.items() if hasattr(LeaveRequest, k)})
    db.add(l)
    db.commit()
    return {"message": "Leave request created"}


@router.put("/leaves/{leave_id}/approve")
def approve_leave(leave_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    l = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Leave request not found")
    l.status = "approved"
    l.approved_by = user.full_name
    db.commit()
    return {"message": "Approved"}
