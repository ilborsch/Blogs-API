from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import ShowLogin
from ..database import get_db
from ..models import User
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..JWT_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter((request.username == User.username) | (request.username == User.email)).first()
    if not user:
        raise HTTPException(detail=f"Invalid account", status_code=status.HTTP_404_NOT_FOUND)

    if not Hash.verify(request.password, user.password):
        raise HTTPException(detail=f"Invalid password", status_code=status.HTTP_404_NOT_FOUND)

    jwt_token = create_access_token(data={'sub': request.username})
    return {"status": "DONE", "access_token": jwt_token, 'token_type': 'bearer'}
