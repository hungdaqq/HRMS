from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from models import User
from schemas import UserLogin, UserCreate, UserUpdate
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["User"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
async def startup_event():

    db = SessionLocal()

    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        db.add(
            User(
                username="admin",
                email="admin@test.com",
                full_name="System Admin",
                title="Admin",
                password=hash_password("123456a@"),
                is_admin=True,
            )
        )
        db.commit()

    test_user = db.query(User).filter(User.username == "test").first()
    if not test_user:
        db.add(
            User(
                username="test",
                email="test@test.com",
                full_name="Test User",
                title="Engineer",
                password=hash_password("123456a@"),
            )
        )
        db.commit()

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
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        title=user.title,
        salary=user.salary,
        profile_image=user.profile_image,
    )
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


@router.get("/user/profile")
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
    if not current_user["is_admin"]:
        return JSONResponse(status_code=403, content={"message": "Forbidden."})

    users = db.query(User).all()

    return JSONResponse(
        status_code=200,
        content={
            "message": "User retrieved successfully.",
            "data": [user.to_dict() for user in users],
        },
    )


@router.put("/user/{user_id}")
async def update_user(
    user_id: str,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return JSONResponse(status_code=404, content={"message": "User not found."})

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()

    db.refresh(db_user)

    return JSONResponse(
        status_code=200,
        content={"message": "User updated successfully.", "data": db_user.to_dict()},
    )
