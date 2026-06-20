from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Login(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    

class ExerciseCreate(BaseModel):
    title: str
    description : str
    category: Literal[
        "Chest",
        "Leg",
        "Back",
        "Shoulder",
        "Arms",
        "Core"
    ]

class WorkoutCreate(BaseModel):
    title: str
    schedule_at: datetime
    comment: str
  
class WorkoutExerciseCreate(BaseModel):
    id_exercise: int 
    sets: int
    reps: int
    weight: int

class WorkoutUpdate(BaseModel):
    new_title: str
    new_schedule: str
    new_comment: str

class WorkoutUpdateStatus(BaseModel):
    status: Literal[
        "pending",
        "completed",
        "cancelled"
    ]

class UserResponse(BaseModel):
    id_user: int
    username: str

class WorkoutResponse(BaseModel):
    id_workout: int
    title: str
    schedule_at: datetime
    comment:str
    status: str
    created_at: datetime
    update_at: datetime

class ExerciseResponse(BaseModel):
    id_exercise: int
    title: str
    description: str
    category: str