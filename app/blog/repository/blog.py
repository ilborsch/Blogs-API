from fastapi import status, HTTPException
from ..models import Blog
from ..schemas import Blog as BlogSchema, ShowUser, BaseBlog
from .user import get_user_id, check_blog_creator
from sqlalchemy.orm import Session


def get_all(db: Session, user: ShowUser):
    return user.blogs


def get_by_id(id: int, db: Session, user: ShowUser):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)
    return blog


def create(request: BaseBlog, db: Session, user: ShowUser):
    new_blog = Blog(title=request.title, body=request.body, creator_id=get_user_id(user, db))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db: Session, user: ShowUser):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)

    # check_blog_creator(blog, db, user)

    query.delete()
    db.commit()
    return {"status": "DONE"}


def update(id: int, request: BaseBlog, db: Session, user: ShowUser):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)

    # check_blog_creator(blog, db, user)

    query.update(dict(request))
    db.commit()
    return {"status": "DONE", "data": query.first()}


