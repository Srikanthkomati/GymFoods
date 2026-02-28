from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    age: int
    height: int
    weight: int
    goal: str
    city: str
    diet_type: str
    budget: str
