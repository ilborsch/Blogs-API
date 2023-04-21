from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(BaseModel):
    username: str
    email: str
    success: bool = True
    
    class Config:
        orm_mode = True


