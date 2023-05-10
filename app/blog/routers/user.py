from fastapi import Depends, status
from app.blog.schemas import User as UserSchema, ShowUser
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter
from ..repository import user
from fastapi_cache.decorator import cache

router = APIRouter(
    tags=['Users'],
    prefix='/api/user'
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}/', status_code=status.HTTP_200_OK, response_model=ShowUser)
@cache(expire=60)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user.get_by_id(id, db)

