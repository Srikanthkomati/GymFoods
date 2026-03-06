from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    goal = Column(String)   # gain or loss
    city = Column(String)
    diet_type = Column(String)
    budget = Column(String)
