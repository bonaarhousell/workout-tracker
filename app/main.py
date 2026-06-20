from fastapi import FastAPI

from app.routers import auth
from app.routers import exercise
from app.routers import workout
from app.routers import report

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
app.include_router(exercise.router, tags=["Exercise"])
app.include_router(workout.router, tags=["Workout"])
app.include_router(report.router, tags=["Report"])