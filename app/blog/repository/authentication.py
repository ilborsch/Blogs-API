from fastapi import status, HTTPException
from ..models import User
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..JWT_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import UserRegistrationSchema


def validate_user(request: UserRegistrationSchema, db: Session):
    is_valid_username = db.query(User).filter(User.username == request.username).first() is None
    is_valid_email = db.query(User).filter(User.email == request.email).first() is None
    return is_valid_username and is_valid_email


def login(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter((request.username == User.username) | (request.username == User.email)).first()
    if not user:
        raise HTTPException(detail=f"Invalid account", status_code=status.HTTP_404_NOT_FOUND)

    if not Hash.verify(request.password, user.password):
        raise HTTPException(detail=f"Invalid password", status_code=status.HTTP_404_NOT_FOUND)

    jwt_token = create_access_token(data={'sub': request.username})
    return {"status": "DONE", "access_token": jwt_token, 'token_type': 'bearer'}


def register(request: UserRegistrationSchema, db: Session):
    if not validate_user(request, db):
        raise HTTPException(detail=f"The user already exists.", status_code=status.HTTP_403_FORBIDDEN)

    if request.password != request.repeated_password:
        raise HTTPException(detail=f"Passwords do not match.", status_code=status.HTTP_403_FORBIDDEN)

    if None in (request.username, request.email):
        raise HTTPException(detail=f"All fields must be filled", status_code=status.HTTP_403_FORBIDDEN)

    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username,
                    email=request.email,
                    password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    login_form = OAuth2PasswordRequestForm(
        username=request.username,
        password=request.password,
        grant_type="",
        scope="",
        client_secret=None,
        client_id=None
    )
    return login(login_form, db)

