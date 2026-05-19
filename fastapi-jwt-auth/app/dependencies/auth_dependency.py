from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.repositories.user_repository import (get_user_by_email)

from app.utils.jwt_handler import (verify_access_token)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")

    user = get_user_by_email(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user