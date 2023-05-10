from fastapi import status, HTTPException
from app.blog.models import Blog
from app.blog.schemas import ShowUser, BaseBlog, BlogSchema
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

    check_blog_creator(blog, db, user)  # comment when test

    query.delete()
    db.commit()
    return {"status": "DONE"}


def full_update(id: int, request: BlogSchema, db: Session, user: ShowUser):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)

    check_blog_creator(blog, db, user)  # comment when test

    query.update({
        "title": request.title if request.title is not None else "",
        "body": request.body if request.body is not None else ""
    })
    db.commit()
    return {"status": "DONE", "data": query.first()}


def partial_update(id: int, request: BlogSchema, db: Session, user: ShowUser):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is None:
        raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)

    check_blog_creator(blog, db, user)  # comment when test

    query.update({
        "title": request.title if request.title is not None else blog.title,
        "body": request.body if request.body is not None else blog.body
    })
    db.commit()
    return {"status": "DONE", "data": query.first()}


