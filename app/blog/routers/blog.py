from typing import List
from fastapi import Depends, status, APIRouter
from ..schemas import Blog as BlogSchema, ShowBlog, ShowUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import blog
from ..oauth2 import get_current_user

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.get_all(db)


@router.get('/{id}/', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def get_blog_by_id(id: int, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.get_by_id(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
def create_blog(request: BlogSchema, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.create(request, db)


@router.delete('/{id}/', status_code=status.HTTP_200_OK)
def delete_blog(id: int, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.delete(id, user, db)


@router.put('/{id}/', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: BlogSchema, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.update(id, request, user, db)


