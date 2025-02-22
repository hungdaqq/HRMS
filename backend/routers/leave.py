from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Leave, User
from schemas import CreateLeave, UpdateLeave
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
        employee_id=current_user["id"],
        date=leave.date,
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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    status: str = Query(None, description="Filter by status."),
):
    if current_user["is_admin"]:
        # If the user is an admin, retrieve all leaves
        query = db.query(Leave, User).join(User, User.id == Leave.employee_id)
    else:
        # If the user is not an admin, filter by the current user's employee ID
        query = (
            db.query(Leave, User)
            .join(User, User.id == Leave.employee_id)
            .filter(Leave.employee_id == current_user["id"])
        )

    # Apply query filters based on the query parameters
    if status:
        query = query.filter(Leave.status == status)

    # Fetch the leaves
    results = query.all()

    # Prepare the data for response
    if results:
        data = [
            {
                "id": str(leave.id),
                "employee_id": str(leave.employee_id),
                "username": user.username,
                "full_name": user.full_name,
                "date": str(leave.date),
                "reason": leave.reason,
                "status": leave.status,
            }
            for leave, user in results
        ]

    else:
        data = None

    return JSONResponse(
        status_code=200,
        content={
            "message": "Leave requests retrieved successfully.",
            "data": data,
        },
    )


@router.put("/leave/{leave_id}")
async def update_leave(
    leave_id: str,
    update: UpdateLeave,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        return JSONResponse(
            status_code=404,
            content={"message": "Leave request not found."},
        )

    if current_user["is_admin"]:
        leave.status = update.status
        db.commit()
        db.refresh(leave)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Leave request updated successfully.",
                "data": leave.to_dict(),
            },
        )
    else:
        return JSONResponse(
            status_code=403,
            content={"message": "Forbidden."},
        )
