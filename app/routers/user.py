from datetime import datetime
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(prefix="/users", tags=["Authenticate"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hash_pass = utils.hash(user.password)
    user.password = hash_pass

    new_user = models.Users(
        api_key=oauth2.create_access_token(
            data={
                "email": user.email,
                "user_id": user.user_id,
                "iat": datetime.utcnow(),
            }
        ),
        **user.dict(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/myaccount", response_model=schemas.User)
def get_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    user = (
        db.query(models.Users)
        .filter(models.Users.user_id == current_user.user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_id={id} does not exist",
        )

    return user
