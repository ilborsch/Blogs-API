import pytest
from sqlalchemy import insert, select
from app.blog.models import User
from .conftest import client, sessionmaker

# create user before
def test_login():
    response = client.post('/login', json={
                "username": "test_client",
                "password": "test_password"
                })
    response_json = response.json()

    assert len(response_json.keys()) == 3
    assert response_json['status'] == 'DONE'



