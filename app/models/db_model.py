from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime   
from app.database.setup_db import Base, engine

class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workouts = relationship(
        "Workout",
        back_populates="user"
    )
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str] 

class Exercise(Base):
    __tablename__ = "exercises"

    id_exercise: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="exercise"
    )
    title: Mapped[str]
    description : Mapped[str]
    category: Mapped[str]

class Workout(Base):
    __tablename__ = "workouts"

    id_workout: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user = relationship(
        "User",
        back_populates="workouts"
    )
    workout_exercise = relationship(
        "WorkoutExercise",
        back_populates="workout"
    )
    id_user: Mapped[int] = mapped_column(
            ForeignKey("users.id_user")
            )
    title: Mapped[str]
    schedule_at: Mapped[datetime]
    comment: Mapped[str]
    status: Mapped[str]
    created_at: Mapped[datetime]
    update_at: Mapped[datetime]

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id_workout_excercise: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout = relationship(
        "Workout",
        back_populates="workout_exercise"
    )
    exercise = relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    id_user: Mapped[int] = mapped_column(
            ForeignKey("users.id_user")
            )
    id_workout: Mapped[int] = mapped_column(
        ForeignKey("workouts.id_workout")
    )
    id_exercise: Mapped[int] = mapped_column(
        ForeignKey("exercises.id_exercise")
    )
    sets: Mapped[int]
    reps: Mapped[int]
    weight: Mapped[int]

Base.metadata.create_all(engine)