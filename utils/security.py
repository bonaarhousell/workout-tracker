from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError
from dotenv import load_dotenv

import os
import jwt
import app.models.db_model as db_model
import app.database.setup_db as setup_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)

def create_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str):
    try:
        access = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return access
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token was expired"
        )


def get_current_user(
        token: str = Depends(oauth2_schema),
        db: Session = Depends(setup_db.get_db)
):
    payload = verify_token(token)

    user = db.get(
        db_model.User,
        payload["user_id"]
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    
    return user