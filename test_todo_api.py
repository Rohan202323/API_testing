""" API Testing """
import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def base_url():
    """It returns the base url."""
    return BASE_URL

def test_get_all_posts(base_url):
    """ It retrives the all post."""
    response = requests.get(f"{base_url}/posts", timeout=10)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_single_post(base_url):
    """ It retrives the one post"""
    post_id = 1
    response = requests.get(f"{base_url}/posts/{post_id}", timeout=10)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    data = response.json()
    print(data)
    assert isinstance(data, dict)
    assert data["id"] == post_id

def test_create_post(base_url):
    """It creates the new post"""
    payload = {
        "title": "famous",
        "body": "bar",
        "userId": 1
    }
    response = requests.post(f"{base_url}/posts", json=payload, timeout=10)
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

def test_update_post(base_url):
    """It updates the existing post """
    post_id = 1
    payload = {
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = requests.put(f"{base_url}/posts/{post_id}", json=payload, timeout=10)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    data = response.json()
    print(data)
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

def test_delete_post(base_url):
    """It deletes the particular post"""
    post_id = 1
    response = requests.delete(f"{base_url}/posts/{post_id}", timeout=10)
    assert response.status_code == 200
    assert response.json() == {}
