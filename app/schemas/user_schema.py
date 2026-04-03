from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# --------------------------------
# Register Schema (Request)
# --------------------------------
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(..., min_length=6)

    age: int = Field(..., gt=0, lt=120)
    height: int = Field(..., gt=50, lt=300)
    weight: int = Field(..., gt=20, lt=500)

    goal: str
    city: str
    diet_type: str
    budget: str


# --------------------------------
# Login Schema (Request)
# --------------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --------------------------------
# Token Response
# --------------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


# --------------------------------
# User Response (Output)
# --------------------------------
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    age: Optional[int]
    height: Optional[int]
    weight: Optional[int]

    goal: Optional[str]
    city: Optional[str]
    diet_type: Optional[str]
    budget: Optional[str]

    class Config:
        from_attributes = True


# --------------------------------
# Profile Update
# --------------------------------
class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    height: Optional[int]
    weight: Optional[int]

    goal: Optional[str]
    city: Optional[str]
    diet_type: Optional[str]
    budget: Optional[str]