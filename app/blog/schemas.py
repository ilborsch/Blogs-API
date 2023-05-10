from pydantic import BaseModel
from typing import List, Optional


class BaseConfig(BaseModel):
    class Config:
        orm_mode = True


class User(BaseConfig):
    username: str
    email: str
    password: str


class BlogSchema(BaseConfig):
    title: Optional[str]
    body: Optional[str]


class BaseBlog(BlogSchema):
    id: int


class ShowCreator(BaseConfig):
    username: str
    email: str


class ShowUser(ShowCreator):
    blogs: List[BaseBlog]


class ShowBlog(BaseBlog):
    creator: ShowCreator


class ShowLogin(BaseConfig):
    username: str
    password: str


class Token(BaseConfig):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserRegistrationSchema(BaseConfig):
    username: str
    email: str
    password: str
    repeated_password: str

