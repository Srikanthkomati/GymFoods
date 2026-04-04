from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from datetime import datetime

from app.db.database import Base


class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)

    quantity = Column(Float, nullable=False)

    meal_type = Column(String, nullable=True)  # breakfast/lunch/dinner/snack

    timestamp = Column(DateTime, default=datetime.utcnow)