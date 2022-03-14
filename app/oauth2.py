from jose import JWTError, jwt
from . import schemas, models, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Request,
)
from fastapi.security.api_key import APIKeyHeader

from app import database
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not Validate Credentials",
)


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: schemas.TokenData):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(req: Request, db: Session = Depends(database.get_db)):
    api_key = req.headers["apikey"]
    token = verify_access_token(api_key)
    user = db.query(models.Users).filter(models.Users.user_id == token.id).first()
    return user
