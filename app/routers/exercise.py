from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Literal
from utils.security import get_current_user

import app.schemas.schemas as schemas
import app.models.db_model as db_model
import app.database.setup_db as setup_db

router = APIRouter()

@router.post("/exercise")
def create_exercise(
    exercise: schemas.ExerciseCreate,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="only admin can create exercise!"
        )
    
    new_exercise = db_model.Exercise(
        title=exercise.title,
        description=exercise.description,
        category=exercise.category
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return {
        "message": "Exercise created",
        "id_exercise": new_exercise.id_exercise
    }

@router.get("/exercise", response_model=list[schemas.ExerciseResponse])
def list_exercise(
    db: Session = Depends(setup_db.get_db)
): 
    exercise = db.query(db_model.Exercise).all()
    return exercise

@router.get("/exercise/category/{category}", response_model=list[schemas.ExerciseResponse])
def filter_exercise_by_category(
        category: Literal[
        "Leg",
        "Arms",
        "Core",
        "Shoulder",
        "Back",
        "Chest"
        ],
        db: Session = Depends(setup_db.get_db)
):
    exercise = db.query(db_model.Exercise).filter(
        db_model.Exercise.category == category
    ).all()

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="exercise not found"
        )
    return exercise