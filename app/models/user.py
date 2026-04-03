from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Authentication
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    # Profile Data
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)

    goal = Column(String)          # gain / loss / maintain
    city = Column(String)
    diet_type = Column(String)
    budget = Column(String)

    # Account Status
    is_active = Column(Boolean, default=True)

    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)