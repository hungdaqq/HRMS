import uuid
from sqlalchemy import Column, String, Boolean, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    title = Column(String)
    salary = Column(Integer)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "title": self.title,
            "is_admin": self.is_admin,
            "salary": self.salary,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
