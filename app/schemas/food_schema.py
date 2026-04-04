from pydantic import BaseModel

# --------------------------------
# Food Schemas
# --------------------------------
class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float = 0
    carbs: float = 0
    fats: float = 0
    category: str = "veg"  # default to veg, can be veg/non-veg/vegan



class FoodCreate(FoodBase):
    pass


class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attributes = True