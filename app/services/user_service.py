def calculate_targets(user):
    weight = user.weight
    height = user.height
    age = user.age

    # 🔥 BMR (Mifflin-St Jeor)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    # 🔥 Activity multiplier
    activity_map = {
        "sedentary": 1.2,
        "moderate": 1.55,
        "active": 1.725
    }

    multiplier = activity_map.get(user.activity_level, 1.2)

    tdee = bmr * multiplier

    # 🔥 Adjust based on goal
    if user.goal == "loss":
        calories = tdee - 400
    elif user.goal == "gain":
        calories = tdee + 400
    else:
        calories = tdee

    # 🔥 Macros (simple split)
    protein = weight * 1.8
    fats = weight * 0.8
    carbs = (calories - (protein * 4 + fats * 9)) / 4

    return {
        "calories": round(calories),
        "protein": round(protein),
        "carbs": round(carbs),
        "fats": round(fats)
    }