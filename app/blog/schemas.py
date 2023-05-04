from pydantic import BaseModel, Field
from typing import List, Optional


class BaseConfig(BaseModel):
    class Config:
        orm_mode = True


class User(BaseConfig):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=50, regex=r"^.*@([\w-]+\.)+[\w-]{2,4}$")
    password: str = Field(min_length=8, max_length=50)


class Blog(BaseConfig):
    title: str = Field(default="Blank Blog title")
    body: str = Field(default="Blank Blog body")
    creator_id: int


class ShowCreator(BaseConfig):
    username: str
    email: str


class ShowUser(ShowCreator):
    blogs: List[Blog]


class ShowBlog(BaseConfig):
    title: str
    body: str
    creator: ShowCreator


class ShowLogin(BaseConfig):
    username: str
    password: str


class Token(BaseConfig):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

