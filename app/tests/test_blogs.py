from app.blog.models import Blog
from app.blog.repository import blog
from .conftest import client, TEST_BLOG
from fastapi import HTTPException


def test_unauthorized_create_blog():
    response = client.post('/blog', json=TEST_BLOG)
    json = response.json()

    assert response.status_code == 401
    assert json['detail'] == 'Not authenticated'


def test_unauthorized_get_all_blogs():
    response = client.post('/blog')
    json = response.json()

    assert response.status_code == 401
    assert json['detail'] == 'Not authenticated'


def test_unauthorized_get_blog():
    response = client.get('/blog/1')
    json = response.json()

    assert response.status_code == 401
    assert json['detail'] == 'Not authenticated'


def test_unauthorized_delete_blog():
    response = client.delete('/blog/1')
    json = response.json()

    assert response.status_code == 401
    assert json['detail'] == 'Not authenticated'


def test_unauthorized_update_blog():
    response = client.put('/blog/1', json=TEST_BLOG.update({"creator_id": 1}))
    json = response.json()

    assert response.status_code == 401
    assert json['detail'] == 'Not authenticated'

