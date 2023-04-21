from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from models import *
from schemas import Blog as BlogSchema, User as UserSchema, ShowUser
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash
import uvicorn


app = FastAPI()

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"success": True, "data": new_blog}


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[BlogSchema])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=BlogSchema)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if blog is None:
        raise HTTPException(detail= f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def delete_blog(id: int, db: Session = Depends(get_db)):
    query = db.query(Blog).filter(Blog.id == id)
    if query.first() is not None:
        query.delete(synchronize_session=False)
        db.commit()
        return {"success": True, "details": "DONE"}
    raise HTTPException(detail= f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    query = db.query(Blog).filter(Blog.id == id)
    blog = query.first()
    if blog is not None:
        query.update(dict(request))
        db.commit()
        return {"success": True, "details": "DONE", "data": query.first()}
    raise HTTPException(detail=f"Blog with id {id} isn't available.", status_code=status.HTTP_404_NOT_FOUND)


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    if len(request.username) < 3 or len(request.password) < 3 or request.email.count('@') < 1:
        raise HTTPException(detail=f"Invalid user form", status_code=status.HTTP_403_FORBIDDEN)

    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser)
def create_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(detail=f"User with the id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    return user


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app=app)

