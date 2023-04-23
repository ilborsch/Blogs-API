from fastapi import Depends, status, Response, HTTPException
from ..models import Blog, User
from ..schemas import Blog as BlogSchema, ShowUser
from ..database import get_db
from sqlalchemy.orm import Session


def get_all(db: Session = Depends(get_db)):
    return db.query(Blog).all()


def get_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if blog is None:
        raise HTTPException(detail= f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)
    return blog


def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body, creator_id=request.creator_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, user: ShowUser, db: Session = Depends(get_db)):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)

    creator = db.query(User).filter(user.username == User.username).first()
    if blog.creator_id != creator.id:
        raise HTTPException(detail=f"Not allowed", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    query.delete()
    db.commit()
    return {"success": True, "details": "DONE"}


def update(id: int, request: BlogSchema, user: ShowUser, db: Session = Depends(get_db)):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)

    creator = db.query(User).filter(user.username == User.username).first()
    if blog.creator_id != creator.id:
        raise HTTPException(detail=f"Not allowed", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    query.update(dict(request))
    db.commit()
    return {"success": True, "details": "DONE", "data": query.first()}


