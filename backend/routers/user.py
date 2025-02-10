from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from models import User
from schemas import UserLogin, UserCreate
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
async def startup_event():
    db = SessionLocal()
    admin_user = db.query(User).filter(User.is_admin == True).first()
    if not admin_user:
        db.add(
            User(
                username="admin",
                email="admin@test.com",
                password=hash_password("123456a@"),
                is_admin=True,
            )
        )
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    test_user = db.query(User).filter(User.username == "test").first()
    if not test_user:
        db.add(
            User(
                username="test",
                email="test@test.com",
                password=hash_password("123456a@"),
            )
        )
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    db.close()


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return JSONResponse(
            status_code=400, content={"message": "Usename already exists."}
        )

    # Hash the password and create a new user
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return JSONResponse(
        status_code=201,
        content={"message": "User created successfully.", "data": db_user.to_dict()},
    )


@router.post("/login")
async def login_user(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        return JSONResponse(
            status_code=400, content={"message": "Invalid credentials."}
        )

    token, expire = create_access_token(
        {"id": str(db_user.id), "is_admin": db_user.is_admin}
    )
    return JSONResponse(
        status_code=200,
        content={
            "access_token": token,
            "expire": str(expire),
            "is_admin": db_user.is_admin,
        },
    )


@router.get("/user/details")
async def get_user(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    return JSONResponse(
        status_code=200,
        content={"message": "User retrieved successfully.", "data": user.to_dict()},
    )


@router.get("/user")
async def get_user(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    users = db.query(User).all()

    return JSONResponse(
        status_code=200,
        content={
            "message": "User retrieved successfully.",
            "data": [user.to_dict() for user in users],
        },
    )
