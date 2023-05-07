from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.blog.database import Base, get_db, SessionLocal
from app.main import app as application
from app.blog.models import User
import pytest

SQLALCHEMY_TEST_DATABASE_PATH = 'sqlite:///../test.db'

engine_test = create_engine(SQLALCHEMY_TEST_DATABASE_PATH, connect_args={
    "check_same_thread": False
})
TestSessionLocal = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine_test)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


application.dependency_overrides[get_db] = override_get_db

client = TestClient(application)

TEST_USER = {
        "username": "test_client",
        "email": "test_email@email.com",
        "password": "password",
        "repeated_password": "password"
}

TEST_BLOG = {
        "title": "title",
        "body": "body"
}


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

