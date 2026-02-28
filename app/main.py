from fastapi import FastAPI
from .database import engine
from . import models
from .routes import auth_routes

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Assistant API")

# Include routers
app.include_router(auth_routes.router)
