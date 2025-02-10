from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Leave
from schemas import CreateLeave
from auth import get_current_user

router = APIRouter(tags=["Leave"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/leave")
async def create_leave(
    leave: CreateLeave,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    leave = Leave(
        employee_id=current_user.id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Leave request submitted successfully.",
            "data": leave.to_dict(),
        },
    )


@router.get("/leave")
async def get_leave(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    leaves = db.query(Leave).filter(Leave.employee_id == current_user.id).all()
    return JSONResponse(
        status_code=200,
        content={
            "message": "Leave requests retrieved successfully.",
            "data": [leave.to_dict() for leave in leaves],
        },
    )
