from fastapi import Depends, status, HTTPException
from ..models import User, Blog
from ..schemas import User as UserSchema, ShowUser, BaseBlog, ShowBlog
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash


def get_user_id(user: ShowUser, db: Session) -> int:
    user_id = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first().id
    return user_id


def check_blog_creator(blog, db: Session, user: ShowUser) -> None:
    creator = db.query(User).filter((user.username == User.username) & (user.email == User.email)).first()
    if blog.creator_id != creator.id:
        raise HTTPException(detail=f"Not allowed", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


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
