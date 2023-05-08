import pytest
from app.blog.models import User
from app.blog.repository import authentication
from .conftest import client, TEST_USER, get_db
from app.blog.models import User
from app.blog.schemas import UserRegistrationSchema


def test_valid_registration(db_session):
    db_session.query(User).filter((User.username == TEST_USER['username']) | (User.email == TEST_USER['email'])).delete()
    db_session.commit()

    response = client.post('/register', json=TEST_USER)

    json = response.json()
    assert response.status_code == 200
    assert json['status'] == 'DONE'


def test_user_already_exists_invalid_registration():
    response = client.post('/register', json=TEST_USER)

    json = response.json()
    assert response.status_code == 403
    assert json['detail'] == 'The user already exists.'


def test_invalid_passwords_registration():
    response = client.post('/register', json={
        "username": "new_test_user",
        "email": "new_test_user@email.com",
        "password": "password",
        "repeated_password": "different password"
    })

    json = response.json()
    assert response.status_code == 403
    assert json['detail'] == 'Passwords do not match.'


def test_validate_user():
    assert authentication.validate_user(request=UserRegistrationSchema(
        username="invalid_user",
        email="invalid_email",
        password="invalid_password",
        repeated_password="invalid_password"
    ), db=next(get_db())) is True

    assert authentication.validate_user(request=UserRegistrationSchema(
        username="invalid_user",
        email=TEST_USER["email"],
        password="invalid_password",
        repeated_password="invalid_password"
    ), db=next(get_db())) is False

    assert authentication.validate_user(request=UserRegistrationSchema(
        username=TEST_USER["username"],
        email="invalid email",
        password="invalid_password",
        repeated_password="invalid_password"
    ), db=next(get_db())) is False


def test_valid_username_login_():
    response = client.post("/login", data={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })

    json = response.json()
    assert json["status"] == "DONE"
    assert response.status_code == 200


def test_valid_email_login_():
    response = client.post("/login", data={
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    })

    json = response.json()
    assert json["status"] == "DONE"
    assert response.status_code == 200


def test_invalid_username_login():
    response = client.post('/login', data={
        "username": "invalid_username",
        "password": TEST_USER["password"]
    })

    json = response.json()
    assert json["detail"] == "Invalid account"
    assert response.status_code == 404


def test_invalid_password_login():
    response = client.post('/login', data={
        "username": TEST_USER["username"],
        "password": "invalid_password"
    })

    json = response.json()
    assert json["detail"] == "Invalid password"
    assert response.status_code == 404

