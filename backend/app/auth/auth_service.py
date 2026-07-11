from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.hashing import hash_password, verify_password


def create_user(
    db: Session,
    full_name: str,
    email: str,
    password: str
):

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return None

    user = User(
        full_name=full_name,
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user