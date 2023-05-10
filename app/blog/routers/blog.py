from fastapi import Depends, status, APIRouter
from fastapi_cache.decorator import cache
from app.blog.schemas import BlogSchema, ShowBlog, ShowUser, BaseBlog
from app.blog.database import get_db
from sqlalchemy.orm import Session
from app.blog.repository import blog
from app.blog.oauth2 import get_current_user

router = APIRouter(
    tags=['Blogs'],
    prefix='/api/blog'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[BaseBlog])
@cache(expire=60)
def get_all_blogs(db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.get_all(db, user)


@router.get('/{id}/', status_code=status.HTTP_200_OK, response_model=ShowBlog)
# @cache(expire=60)
def get_blog_by_id(id: int, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.get_by_id(id, db, user)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
def create_blog(request: BaseBlog, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.create(request, db, user)


@router.delete('/{id}/', status_code=status.HTTP_200_OK)
def delete_blog(id: int, db: Session = Depends(get_db), user: ShowUser = Depends(get_current_user)):
    return blog.delete(id, db, user)


@router.put('/{id}/', status_code=status.HTTP_202_ACCEPTED)
def full_update_blog(id: int, request: BlogSchema,
                     db: Session = Depends(get_db),
                     user: ShowUser = Depends(get_current_user)):
    return blog.full_update(id, request, db, user)


@router.patch('/{id}/', status_code=status.HTTP_202_ACCEPTED)
def partial_update_blog(id: int, request: BlogSchema,
                        db: Session = Depends(get_db),
                        user: ShowUser = Depends(get_current_user)):
    return blog.partial_update(id, request, db, user)



