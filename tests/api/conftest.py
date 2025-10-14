import pytest
import httpx
from faker import Faker
from config.settings import settings
from core.logger import logging

logger = logging.getLogger(__name__)
faker = Faker()


@pytest.fixture(scope="session")
def base_url():
    return settings.API_BASE_URL

@pytest.fixture(scope="session")
def http_client(base_url):
    client = httpx.Client(base_url=base_url,timeout=30.0)
    yield client
    client.close()

@pytest.fixture(scope="function")
def new_user(http_client):
    user_data = {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(10)
    }
    response = http_client.post("/users", json=user_data)
    assert response.status_code == 201, f"Failed to create user: {response.text}"

    user_response = response.json()
    token = user_response.get("token")

    result = {
        "user": user_response.get("user"),
        "token": token,
        "password": user_data["password"],
        "email": user_data["email"]
    }

    yield result

    delete_response = http_client.delete(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"})
    if delete_response.status_code != 200:
        logger.warning(
        f"Failed to delete user {user_data['email']}. "
        f"Status: {delete_response.status_code}, "
        f"Response: {delete_response.text}"
    )


@pytest.fixture(scope="function")
def auth_headers(new_user):
    return {"Authorization": f"Bearer {new_user['token']}"}