from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_PATH = 'sqlite:///../blog.db'

engine = create_engine(SQLALCHEMY_DATABASE_PATH, connect_args={
    "check_same_thread": False
})

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
