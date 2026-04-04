from pydantic import BaseModel
from datetime import datetime


class MealBase(BaseModel):
    user_id: int
    food_id: int
    quantity: float
    meal_type: str | None = None


class MealCreate(MealBase):
    pass


class MealResponse(MealBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True