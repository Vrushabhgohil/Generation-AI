import uuid
from sqlalchemy import Column, String, DateTime,Boolean
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    auth_type = Column(String, nullable=False, default='Manual')
    google_id = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_activate = Column(Boolean, nullable=True)
    is_verified = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, nullable=False)
