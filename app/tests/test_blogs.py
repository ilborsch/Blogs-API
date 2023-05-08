import pytest
from app.blog.models import Blog
from .conftest import client, TEST_BLOG, TEST_USER


# Unauthorized


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


# Authorized


def test_authorized_create_blog(authorized_user: dict, db_session):
    db_session.query(Blog).filter((Blog.body == TEST_BLOG['body']) | (Blog.title == TEST_BLOG['title'])).delete()
    db_session.commit()

    response = client.post('/blog', json=TEST_BLOG,
                           headers={"Authorization": f"Bearer {authorized_user['access_token']}"})
    json = response.json()
    if TEST_BLOG['id'] is None: TEST_BLOG['id'] = json['id']

    assert response.status_code == 201
    assert json['title'] == TEST_BLOG['title']
    assert json['body'] == TEST_BLOG['body']
    assert json['creator'] == {
        'username': TEST_USER['username'],
        'email': TEST_USER['email']
    }


def test_authorized_get_all_blogs(authorized_user: dict):
    response = client.get('/blog',
                          headers={"Authorization": f"Bearer {authorized_user['access_token']}"})
    json = response.json()
    the_blog = json[0]

    assert response.status_code == 200
    assert the_blog['title'] == TEST_BLOG['title']
    assert the_blog['body'] == TEST_BLOG['body']


def test_authorized_get_blog(authorized_user: dict):
    response = client.get(f'/blog/{TEST_BLOG["id"]}',
                          headers={"Authorization": f"Bearer {authorized_user['access_token']}"})
    json = response.json()

    assert response.status_code == 200
    assert json['title'] == TEST_BLOG['title']
    assert json['body'] == TEST_BLOG['body']


def test_authorized_update_blog(authorized_user):
    response = client.put(f'/blog/{TEST_BLOG["id"]}',
                          headers={"Authorization": f"Bearer {authorized_user['access_token']}"},
                          json={
                              'title': 'new_title',
                              'body': 'new_body'
                          })
    json = response.json()
    TEST_BLOG['title'] = 'new_title'
    TEST_BLOG['body'] = 'new_body'
    the_blog = json['data']

    assert response.status_code == 202
    assert json['status'] == 'DONE'
    assert the_blog['title'] == TEST_BLOG['title']
    assert the_blog['body'] == TEST_BLOG['body']


def test_authorized_delete_blog(authorized_user):
    response = client.delete(f'/blog/{TEST_BLOG["id"]}',
                             headers={"Authorization": f"Bearer {authorized_user['access_token']}"})
    json = response.json()

    assert response.status_code == 200
    assert json['status'] == 'DONE'

