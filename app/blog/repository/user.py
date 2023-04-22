from fastapi import Depends, status, HTTPException
from ..models import User
from ..schemas import User as UserSchema
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash


def create(request: UserSchema, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(detail=f"User with the id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    return user
