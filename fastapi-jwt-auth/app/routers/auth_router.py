from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.user_schema import (UserCreate, UserResponse, UserLogin, Token )

from app.database.dependencies import get_db

from app.repositories.user_repository import (get_user_by_email, create_user)

from app.utils.hashing import hash_password, verify_password

from app.utils.jwt_handler import (create_access_token)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/test")
def test():

    return {
        "message": "Auth Router Working"
    }


@router.post(
    "/signup",
    response_model=UserResponse
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check existing user
    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    # Create user
    new_user = create_user(
        db=db,
        email=user.email,
        password=hashed_password
    )

    return new_user

@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user
    existing_user = get_user_by_email(
        db,
        user.email
    )

    # Validate email
    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Validate password
    valid_password = verify_password(
        user.password,
        existing_user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Generate JWT token
    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }