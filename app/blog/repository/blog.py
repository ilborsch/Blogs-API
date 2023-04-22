from fastapi import Depends, status, Response, HTTPException
from ..models import Blog
from ..schemas import Blog as BlogSchema
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


def delete(id: int, db: Session = Depends(get_db)):
    query = db.query(Blog).filter(Blog.id == id)
    if query.first() is not None:
        query.delete()
        db.commit()
        return {"success": True, "details": "DONE"}
    raise HTTPException(detail= f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)


def update(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is not None:
        query.update(dict(request))
        db.commit()
        return {"success": True, "details": "DONE", "data": query.first()}
    raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)


