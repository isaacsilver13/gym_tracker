from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, exercises, health, routines
from app.config import load_settings
from app.error_log import install as install_error_log

install_error_log()

app = FastAPI(title="Gym Tracker API", version="0.1.0")

settings = load_settings()
if settings.app_env == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(routines.router, prefix="/api/v1")
app.include_router(exercises.router, prefix="/api/v1")
