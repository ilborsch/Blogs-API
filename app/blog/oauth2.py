from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .JWT_token import verify_token
from .database import get_db
from .models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    current_user_username = verify_token(token, credentials_exception)
    db = next(get_db())
    current_user = db.query(User).filter(User.username == current_user_username).first()
    if current_user is None:
        raise credentials_exception

    return current_user






