from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Attendance, User
from schemas import CreateAttendance
from auth import get_current_user

router = APIRouter(tags=["Attendance"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/attendance")
async def create_attendance(
    attendance: CreateAttendance,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    attendance = Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status,
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Attendance submitted successfully.",
            "data": attendance.to_dict(),
        },
    )


@router.get("/attendance")
async def get_attendance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user["is_admin"]:
        # If the user is an admin, retrieve all attendance
        query = db.query(Attendance, User).join(User, User.id == Attendance.employee_id)
    else:
        # If the user is not an admin, filter by the current user's employee ID
        query = (
            db.query(Attendance, User)
            .join(User, User.id == Attendance.employee_id)
            .filter(Attendance.employee_id == current_user["id"])
        )

    attendance = query.all()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Attendance retrieved successfully.",
            "data": [a.to_dict() for a in attendance],
        },
    )
