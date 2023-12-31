import pytest
import json
from src.api.services.user_service_impl import UserServiceImpl
from src.api.models.users import User
from src.api.interfaces.exceptions.email_already_registered_exception import EmailAlreadyRegisteredException
from src.api.interfaces.exceptions.user_not_found_exception import UserNotFoundException


## --------       CREATE USER     --------


def test_create_user(test_client, monkeypatch):
    user = User(username="test", email="test@test.com", password="12345678")
    user.id = 1

    def mock_create_user(self, username, email, password):
        return user

    monkeypatch.setattr(UserServiceImpl, "create_user", mock_create_user)

    resp = test_client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test",
                "email": "test@test.com",
                "password": "12345678",
            }
        ),
        content_type="application/json",
    )

    data = json.loads(resp.data)
    assert resp.status_code == 201
    assert user.id == data["id"]
    assert user.username == data["username"]
    assert user.email == data["email"]
    assert "password" not in data


def test_create_user_with_email_already_register(test_client, monkeypatch):
    user = User(username="test", email="test@test.com", password="12345678")
    user.id = 1

    def mock_create_user(self, username, email, password):
        raise EmailAlreadyRegisteredException(email=email)

    monkeypatch.setattr(UserServiceImpl, "create_user", mock_create_user)

    resp = test_client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test",
                "email": "test@test.com",
                "password": "12345678",
            }
        ),
        content_type="application/json",
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert f"The email test@test.com is already in use." == data["message"]


def test_create_user_missing_username(test_client, monkeypatch):

    def mock_create_user(self, username, email, password):
        return None

    monkeypatch.setattr(UserServiceImpl, "create_user", mock_create_user)

    resp = test_client.post(
        "/users",
        data=json.dumps(
            {
                "email": "test@test.com",
                "password": "12345678",
            }
        ),
        content_type="application/json",
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid input" == data["error"]


def test_create_user_missing_password(test_client, monkeypatch):


    def mock_create_user(self, username, email, password):
        return None

    monkeypatch.setattr(UserServiceImpl, "create_user", mock_create_user)

    resp = test_client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test",
                "email": "test@test.com",
            }
        ),
        content_type="application/json",
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid input" == data["error"]


def test_create_user_missing_email(test_client, monkeypatch):

    def mock_create_user(self, username, email, password):
        return None

    monkeypatch.setattr(UserServiceImpl, "create_user", mock_create_user)

    resp = test_client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test",
                "password": "12345678",
            }
        ),
        content_type="application/json",
    )

    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 400
    assert "Invalid input" == data["error"]


# ## --------       GET USER     --------


def test_get_existing_user_by_id(test_client, monkeypatch):
    user = User(username="test", email="test@test.com", password="12345678")
    user.id = 1

    def mock_get_user_by_id(self, user_id):
        return user

    monkeypatch.setattr(UserServiceImpl, "get_user_by_id", mock_get_user_by_id)
    resp = test_client.get("/users/1")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 1 == data["id"]
    assert "test" == data["username"]
    assert "test@test.com" == data["email"]
    assert "password" not in data


def test_get_non_existing_user_by_id(test_client, monkeypatch):
    def mock_get_user_by_id(self, user_id):
        raise UserNotFoundException(user_id)

    monkeypatch.setattr(UserServiceImpl, "get_user_by_id", mock_get_user_by_id)
    resp = test_client.get("/users/1")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 404


# ## --------       UPDATE USER     --------


def test_update_user(test_client, monkeypatch):
    user_updated = User(username="test", email="test@test.com", password="12345678")
    user_updated = 1
 

    def mock_update_user(self, username, email, password):
        return user_updated

    monkeypatch.setattr(UserServiceImpl, "update_user", mock_update_user)

    resp = test_client.put(
        "/users/1",
        data=json.dumps(
            {
                "username": "test",
                "password": "12345678",
            }
        ),
        content_type="application/json",
    )

    assert resp.status_code == 204
    assert not resp.data


def test_update_not_existing_user(test_client, monkeypatch):
    user = User(username="test", email="test@test.com", password="12345678")
    user.id = 1

    def mock_update_user(self, user_id, email, password):
        raise UserNotFoundException(user_id)


    monkeypatch.setattr(UserServiceImpl, "update_user", mock_update_user)

    resp = test_client.put(
        "/users/1",
        data=json.dumps(
            {
                "username": "test",
                "email": "test@test.com",
                "password": "12345678",
            }
        ),
        content_type="application/json",
    )

    assert resp.status_code == 404
