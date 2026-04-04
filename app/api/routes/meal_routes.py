from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.meal_schema import MealCreate, MealResponse
from app.services import meal_service

router = APIRouter(tags=["Meals"])


@router.post("/", response_model=MealResponse)
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    return meal_service.create_meal(db, meal)


@router.get("/user/{user_id}", response_model=list[MealResponse])
def get_user_meals(user_id: int, db: Session = Depends(get_db)):
    return meal_service.get_meals_by_user(db, user_id)

@router.get("/summary/{user_id}")
def get_summary(user_id: int, db: Session = Depends(get_db)):
    return meal_service.get_daily_summary(db, user_id)

@router.get("/dashboard/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    return meal_service.get_dashboard(db, user_id)