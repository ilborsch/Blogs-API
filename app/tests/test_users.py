import pytest
from .conftest import client, TEST_USER
from app.blog.repository import user
from app.blog.schemas import ShowUser
from app.blog.models import User


def test_create_user(db_session):
    db_session.query(User)\
        .filter((User.username == TEST_USER['username']) | (User.email == TEST_USER['email'])).delete()
    db_session.commit()

    response = client.post('/user', json={
        "username": TEST_USER['username'],
        "email": TEST_USER['email'],
        "password": TEST_USER['password']
    })
    json = response.json()
    if TEST_USER['id'] is None:
        TEST_USER['id'] = json['id']

    assert json['username'] == TEST_USER['username']
    assert json['email'] == TEST_USER['email']


def test_get_user():
    response = client.get(f'/user/{TEST_USER["id"]}')
    json = response.json()

    assert json['username'] == TEST_USER['username']
    assert json['email'] == TEST_USER['email']


def test_get_user_id_tool(db_session):
    user_id = user.get_user_id(ShowUser(
        username=TEST_USER['username'],
        email=TEST_USER['email'],
        blogs=[]), db_session)

    assert user_id == TEST_USER['id']

