from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.food_schema import FoodCreate, FoodResponse
from app.services import food_service

router = APIRouter(tags=["Foods"])


@router.post("/", response_model=FoodResponse)
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    print("FOOD ROUTES LOADED")
    return food_service.create_food(db, food)


@router.get("/", response_model=list[FoodResponse])
def get_foods(db: Session = Depends(get_db)):
    return food_service.get_all_foods(db)


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    return food_service.get_food_by_id(db, food_id)