from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db, engine
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authenticate"])


@router.post("/auth")
def auth(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.Users)
        .filter(models.Users.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail=f"Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail=f"Invalid Credentials"
        )

    access_token = user.api_key

    return {"API_Key": access_token}
