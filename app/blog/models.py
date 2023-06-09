from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title})>"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    

    blogs = relationship("Blog", back_populates="creator")

    def __repr__(self):
        return f"<User (id={self.id}, username={self.username}, email={self.email})>"
