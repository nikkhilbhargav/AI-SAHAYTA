from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.user import (
    UserRegister,
    UserLogin
)

from app.auth.auth_service import (
    create_user,
    authenticate_user
)

from app.auth.jwt_handler import create_access_token
from app.auth.current_user import get_current_user

from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================================
# Register
# ==========================================================

@router.post("/register")
def register(
    request: UserRegister,
    db: Session = Depends(get_db)
):

    user = create_user(
        db=db,
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    return {
        "message": "User Registered Successfully",
        "user_id": user.id,
        "full_name": user.full_name,
        "email": user.email
    }


# ==========================================================
# JSON Login
# Used by React / Flutter / Mobile / Postman
# ==========================================================

@router.post("/login")
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================================
# OAuth2 Login
# Used only by Swagger Authorize Button
# ==========================================================

@router.post("/token")
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================================
# Current User Profile
# ==========================================================

@router.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "is_active": current_user.is_active
    }