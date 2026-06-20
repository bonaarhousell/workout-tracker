from sqlalchemy.orm import Session
import app.database.setup_db as setup_db
import app.models.db_model as db_model 

db = setup_db.SessionLocal()

exercises = [
    {
        "title": "Bench Press",
        "description": "Chest exercise",
        "category": "Chest"
    },
    {
        "title": "Incline Bench Press",
        "description": "Chest exercise",
        "category": "Chest"
    },
    {
        "title": "Push Up",
        "description": "Chest exercise",
        "category": "Chest",
    },
    {
        "title": "Dumbbell Fly",
        "description": "Chest exercise",
        "category": "Chest"
    },
    {
        "title": "Squat",
        "description": "Leg exercise",
        "category": "Leg"
    },
    {
        "title": "Leg Press",
        "description": "Leg exercise",
        "category": "Leg"
    },
    {
        "title": "Romanian Deadlift",
        "description": "Leg exercise",
        "category": "Leg"
    },
    {
        "title": "Lunges",
        "description": "Leg exercise",
        "category": "Leg"
    },
    {
        "title": "Leg Curl",
        "description": "Leg exercise",
        "category": "Leg"
    },
    {
        "title": "Leg Extension",
        "description": "Leg exercise",
        "category": "Leg"
    },
    {
        "title": "Deadlift",
        "description": "Back exercise",
        "category": "Back"
    },
    {
        "title": "Pull Up",
        "description": "Back exercise",
        "category": "Back"
    },
    {
        "title": "Lat Pulldown",
        "description": "Back exercise",
        "category": "Back"
    },
    {
        "title": "Barbell Row",
        "description": "Back exercise",
        "category": "Back"
    },
    {
        "title": "Overhead Press",
        "description": "Shoulder exercise",
        "category": "Shoulder"
    },
    {
        "title": "Lateral Raise",
        "description": "Shoulder exercise",
        "category": "Shoulder"
    },
    {
        "title": "Front Raise",
        "description": "Shoulder exercise",
        "category": "Shoulder"
    },
    {
        "title": "Barbell Curl",
        "description": "Arms exercise",
        "category": "Arms"
    },
    {
        "title": "Hammer Curl",
        "description": "Arms exercise",
        "category": "Arms"
    },
    {
        "title": "Tricep Pushdown",
        "description": "Arms exercise",
        "category": "Arms"
    },
    {
        "title": "Skull Crusher",
        "description": "Arms exercise",
        "category": "Arms"
    },
    {
        "title": "Plank",
        "description": "Core exercise",
        "category": "Core"
    },
    {
        "title": "Crunch",
        "description": "Core exercise",
        "category": "Core"
    },
    {
        "title": "Leg Raise",
        "description": "Core exercise",
        "category": "Core"
    },
    {
        "title": "Russian Twist",
        "description": "Core exercise",
        "category": "Core"
    }
]


for exercise in exercises:
    existing = db.query(db_model.Exercise).filter(
        db_model.Exercise.title == exercise["title"]
    ).first()

    if existing:
        continue

    db.add(
        db_model.Exercise(
            title=exercise["title"],
            description=exercise["description"],
            category=exercise["category"]
        )
    )

db.commit()