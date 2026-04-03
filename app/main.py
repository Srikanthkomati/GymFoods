from fastapi import FastAPI

from app.db.database import engine
from app.models import user
from app.api.routes import auth_routes, user_routes


# -----------------------------
# Create database tables
# -----------------------------
user.Base.metadata.create_all(bind=engine)


# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(
    title="Fitness Assistant API",
    description="Backend API for GymFoods Fitness Assistant",
    version="1.0.0"
)


# -----------------------------
# Include API Routers
# -----------------------------
app.include_router(
    auth_routes.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    user_routes.router,
    prefix="/api/v1/users",
    tags=["Users"]
)
