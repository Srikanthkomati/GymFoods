from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.db.database import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)

    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)

    category = Column(String, nullable=True)   # veg / non-veg / vegan

    created_at = Column(DateTime, default=datetime.utcnow)