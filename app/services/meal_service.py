from sqlalchemy.orm import Session
from app.models.meal import MealLog
from app.models.food import Food
from app.models.user import User
from app.services.user_service import calculate_targets
from datetime import datetime, timedelta

def create_meal(db: Session, meal):
    db_meal = MealLog(**meal.model_dump())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


def get_meals_by_user(db: Session, user_id: int):
    return db.query(MealLog).filter(MealLog.user_id == user_id).all()

def get_daily_summary(db: Session, user_id: int):
    # Get today's start and end
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    meals = (
        db.query(MealLog)
        .filter(
            MealLog.user_id == user_id,
            MealLog.timestamp >= today_start,
            MealLog.timestamp < today_end
        )
        .all()
    )

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    for meal in meals:
        food = db.query(Food).filter(Food.id == meal.food_id).first()

        if not food:
            continue

        total_calories += food.calories * meal.quantity
        total_protein += food.protein * meal.quantity
        total_carbs += food.carbs * meal.quantity
        total_fats += food.fats * meal.quantity

    return {
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fats": total_fats
    }


def get_dashboard(db: Session, user_id: int):
    summary = get_daily_summary(db, user_id)

    user = db.query(User).filter(User.id == user_id).first()

    targets = calculate_targets(user)

    return {
        "calories": {
            "consumed": summary["calories"],
            "target": targets["calories"],
            "remaining": targets["calories"] - summary["calories"]
        },
        "protein": {
            "consumed": summary["protein"],
            "target": targets["protein"]
        },
        "carbs": {
            "consumed": summary["carbs"],
            "target": targets["carbs"]
        },
        "fats": {
            "consumed": summary["fats"],
            "target": targets["fats"]
        }
    }