from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.security import get_current_user

import app.models.db_model as db_model
import app.database.setup_db as setup_db

router = APIRouter()

@router.get("/report")
def show_report(
    current_user: db_model.User = Depends(get_current_user),
    db: Session = Depends(setup_db.get_db)
):
    report_workout = db.query(db_model.Workout).filter(
        db_model.Workout.id_user == current_user.id_user,
    ).all()

    completed = 0
    pending = 0
    cancelled = 0
    for workout in report_workout:
        
        if workout.status == "completed":
            completed += 1
        elif workout.status == "pending":
            pending += 1
        elif workout.status == "cancelled":
            cancelled += 1

    return {
        "total_workout": len(report_workout),
        "completed_workout": completed,
        "pending_workout": pending,
        "cancelled_workout": cancelled
    }