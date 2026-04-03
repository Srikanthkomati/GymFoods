from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models.refresh_token import RefreshToken
from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.core.security import create_access_token, create_refresh_token, verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Register
# -----------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        age=user.age,
        height=user.height,
        weight=user.weight,
        goal=user.goal,
        city=user.city,
        diet_type=user.diet_type,
        budget=user.budget
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -----------------------------
# Login
# -----------------------------
@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    db_refresh = RefreshToken(
    user_id=user.id,
    token=refresh_token,
    expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(db_refresh)
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# -----------------------------
# Refresh Token
# -----------------------------
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    user_id = verify_token(refresh_token, expected_type="refresh")

    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=401, 
            detail="Refresh token invalid"
        )
    new_access_token = create_access_token(
        data={"sub": user_id}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

# -----------------------------
# log out
# -----------------------------
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):

    user_id = verify_token(refresh_token, expected_type="refresh")

    db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).delete()

    db.commit()

    return {"message": "Logged out successfully"}