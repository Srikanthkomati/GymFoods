from sqlalchemy.orm import Session
from app.models.food import Food
from app.schemas.food_schema import FoodCreate


def create_food(db: Session, food: FoodCreate):
    db_food = Food(**food.model_dump())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


def get_all_foods(db: Session):
    return db.query(Food).all()


def get_food_by_id(db: Session, food_id: int):
    return db.query(Food).filter(Food.id == food_id).first()