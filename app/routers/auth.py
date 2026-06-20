from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.security import create_access_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import bcrypt
import app.models.db_model as db_model
import app.schemas.schemas as schemas
import app.database.setup_db as setup_db

router = APIRouter()

@router.post("/login",status_code=200)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(setup_db.get_db)
):
    user = db.query(db_model.User).filter(
        db_model.User.username == form_data.username
    ).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password "
        )
    if not bcrypt.checkpw(
        form_data.password.encode(),
        user.password_hash.encode()
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )
    token = create_access_token(user.id_user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expired": 3600
    }

@router.post("/register", status_code=201)
def register(
    user: schemas.UserCreate, 
    db: Session = Depends(setup_db.get_db)
):
    existing_user = db.query(db_model.User).filter(
        db_model.User.username == user.username
    ).all()

    if existing_user:
        raise HTTPException(
            status_code=401,
            detail="Username already use"
        )
    hashed_password = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode()
    new_user = db_model.User( 
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Created",
        "id": new_user.id_user
    }