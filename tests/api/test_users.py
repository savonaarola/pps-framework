import pytest 
from faker import Faker
from core.logger import logging
import allure 


logger = logger = logging.getLogger(__name__)
faker = Faker()


@pytest.mark.api
@allure.feature("Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_user(http_client, new_user):
    json = {
        "email": new_user.get("email"),
        "password": new_user.get("password")
    }
    r = http_client.post("/users/login", json=json)
    logger.info(f"Response json: {r.json()}")
    assert r.status_code == 200
    assert r.json().get("firstName") == new_user.get("firstName")
    assert "token" in r.json()


@pytest.mark.api
@allure.feature("Registration")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_add_user(http_client):

    user_data = {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(10)
    }
    logger.info(f"Creating user with data: {user_data}")
    r = http_client.post("/users", json=user_data)
    assert r.status_code == 201
    assert "token" in r.json()
    logger.info(f"Created user: {r.json().get("user").get("firstName")} {r.json().get("user").get("lastName")}, {r.json().get("user").get("email")}")
    
    token = r.json()["token"]
    http_client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})

    

@pytest.mark.api
@allure.feature("Update")
@allure.severity(allure.severity_level.NORMAL)
def test_update_user(http_client, new_user, auth_headers):
    logger.info(f"Existing user: {new_user.get("user").get("firstName")} {new_user.get("user").get("lastName")} {new_user.get("email")}")

    update_data = {
        "email": "test@test.com"
    }
    logger.info(f"Updating email to {update_data['email']}")
    r = http_client.patch("/users/me", json=update_data, headers=auth_headers)
    assert r.status_code == 400
    logger.info(f"Response: {r.json()}")


@pytest.mark.api
@allure.feature("Update")
@allure.severity(allure.severity_level.NORMAL)
def test_update_user_with_someone_email(http_client, new_user, auth_headers):
    logger.info(f"Existing user: {new_user.get("user").get("firstName")} {new_user.get("user").get("lastName")} {new_user.get("email")}")

    update_data = {
        "lastName": faker.last_name(),
        "email": faker.email()
    }
    logger.info(f"Updating lastname to: {update_data['lastName']}, and email to {update_data['email']}")
    r = http_client.patch("/users/me", json=update_data, headers=auth_headers)
    assert r.status_code == 200
    assert r.json().get("lastName") == update_data.get("lastName")
    assert r.json().get("email") == update_data.get("email")
    logger.info(f"Response: {r.json()}")


@pytest.mark.api
@allure.feature("Logout")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_user_logout(http_client, auth_headers):

    r = http_client.post("/users/logout", headers=auth_headers)
    assert r.status_code == 200







@pytest.mark.api
@allure.feature("Unauthorized access")
class TestUserUnauthorized:

    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_profile_unauthorized(self, http_client):
        r = http_client.get("/users/me")
        assert r.status_code == 401
        assert r.json().get("error") == "Please authenticate."

    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_unauthorized(self, http_client):
        r = http_client.patch("/users/me")
        assert r.status_code == 401
        assert r.json().get("error") == "Please authenticate."

    @allure.severity(allure.severity_level.NORMAL)
    def test_logout_user_unauthorized(self, http_client):
        r = http_client.post("/users/logout")
        assert r.status_code == 401
        assert r.json().get("error") == "Please authenticate."

    @allure.severity(allure.severity_level.NORMAL)
    def test_login_user_unauthorized(self, http_client):
        r = http_client.post("/users/login")
        assert r.status_code == 401
        

    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_unauthorized(self, http_client):
        r = http_client.delete("/users/me")
        assert r.status_code == 401
        assert r.json().get("error") == "Please authenticate."



