from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.security import get_current_user
from datetime import datetime
from typing import Literal

import app.schemas.schemas as schemas
import app.models.db_model as db_model
import app.database.setup_db as setup_db

router = APIRouter()
@router.post("/workout")
def create_workout(
    workout: schemas.WorkoutCreate,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    new_workout = db_model.Workout(
        id_user=current_user.id_user,
        title=workout.title,
        schedule_at=workout.schedule_at,
        comment=workout.comment,
        status="pending",
        created_at=datetime.now(),
        update_at=datetime.now()
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return {
        "message": "Workout created",
        "id_workout": new_workout.id_workout
    }

@router.post("/workout/{id_workout}/exercise")
def workout_to_exercise(
    id_workout: int,
    workour_exercise: schemas.WorkoutExerciseCreate,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)   
):
    workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_workout == id_workout
    ).first()
    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    
    if workout.id_user != current_user.id_user:
        raise HTTPException(
            status_code=403,
            detail="access denied"
        )
    exercise = db.query(db_model.Exercise).filter(
        db_model.Exercise.id_exercise == workour_exercise.id_exercise
    ).first()
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )
    workour_to_exercise = db_model.WorkoutExercise(
        id_user=current_user.id_user,
        id_workout=id_workout,
        id_exercise=workour_exercise.id_exercise,
        sets=workour_exercise.sets,
        reps=workour_exercise.reps,
        weight=workour_exercise.weight  
    )
    db.add(workour_to_exercise)
    db.commit()
    db.refresh(workour_to_exercise)
    return {"message": "Exercise added succesfully to Workout"}

@router.get("/workout",response_model=list[schemas.WorkoutResponse])
def list_all_workout(
    current_user: db_model.User = Depends(get_current_user),
    db : Session = Depends(setup_db.get_db)
):
    workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_user == current_user.id_user
    ).all()
    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    return workout

@router.get("/workout/{id_workout}")
def list_detail_workout(
    id_workout: int,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_user == current_user.id_user,
        db_model.Workout.id_workout == id_workout
    ).first()
    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    workout_exercise = db.query(db_model.WorkoutExercise).filter(
        db_model.WorkoutExercise.id_workout == id_workout
    ).all()
    
    exercise_list = []
    for item in workout_exercise:
        exercise = db.get(db_model.Exercise, item.id_exercise)
        exercise_list.append({
            "exercise_name": exercise.title,
            "sets": item.sets,
            "reps": item.reps,
            "weight": item.weight
        })

    return {
        "id_workout": id_workout,
        "title": workout.title,
        "schedule_at": workout.schedule_at,
        "comment": workout.comment,
        "status": workout.status,
        "exercise": exercise_list
    }

@router.put("/workout/{id_workout}")
def update_workout(
    id_workout: int,
    update_workout: schemas.WorkoutUpdate,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    new_workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_workout == id_workout,
        db_model.Workout.id_user == current_user.id_user
    ).first()

    if not new_workout:
        raise HTTPException(
            status_code=404,
            detail="Workout Not Found"
        )
    new_workout.title = update_workout.new_title
    new_workout.schedule_at = update_workout.new_schedule
    new_workout.comment = update_workout.new_comment
    new_workout.update_at = datetime.now()

    db.commit()
    db.refresh(new_workout)
    return {"message": "Workout Update successfully"}

@router.put("/workout/{id_workout}/status")
def update_workout_status(
    id_workout: int,
    new_status: schemas.WorkoutUpdateStatus,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_user == current_user.id_user,
        db_model.Workout.id_workout == id_workout
    ).first()
    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    workout.status = new_status.status
    db.commit()
    db.refresh(workout)
    return {"message": "Status updated!"}

@router.delete("/workout/{id_workout}")
def remove_workout(
    id_workout: int,
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    del_workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_user == current_user.id_user,
        db_model.Workout.id_workout == id_workout
    ).first()

    if not del_workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    
    db.query(db_model.WorkoutExercise).filter(
        db_model.WorkoutExercise.id_workout == id_workout
    ).delete()
    db.delete(del_workout)
    db.commit()
    return {"message": "Workout removed"}

@router.get("/workout/status/{status}", response_model=list[schemas.WorkoutResponse])
def filter_workout_by_status(
    status: Literal["completed", "cancelled", "pending"],
    current_user: db_model.User = Depends(get_current_user),
    db : Session = Depends(setup_db.get_db)
):
    workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_user == current_user.id_user,
        db_model.Workout.status == status
    ).all()
    
    if not workout:
        raise HTTPException(
            status_code=404,
            detail="workout not found"
        )
    
    return workout