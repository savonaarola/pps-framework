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

    logger.info(f"Created user: {response.json().get("user").get("firstName")} {response.json().get("user").get("lastName")}, {response.json().get("user").get("email")}")
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
    logger.info(f"Deleted user: {user_data.get("firstName")} {user_data.get("lastName")}, {user_data.get("email")}")
    if delete_response.status_code != 200:
        logger.warning(
        f"Failed to delete user {user_data['email']}. "
        f"Status: {delete_response.status_code}, "
        f"Response: {delete_response.text}"
    )


@pytest.fixture(scope="function")
def auth_headers(new_user):
    return {"Authorization": f"Bearer {new_user['token']}"}


@pytest.fixture(scope="function")
def contact_data():
    
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "birthdate": faker.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
        "email": faker.email(),
        "phone": faker.numerify('800%%%%%%%'),
        "street1": faker.street_address(),
        "street2": faker.secondary_address(),
        "city": faker.city(),
        "stateProvince": faker.state_abbr(),
        "postalCode": faker.postcode(),
        "country": faker.country_code(representation="alpha-3")
    }

@pytest.fixture(scope="function")
def new_contact(http_client,auth_headers,contact_data):
    logger.info(f"Creating contact: {contact_data['firstName']} {contact_data['lastName']}")
    r = http_client.post("/contacts", json=contact_data,headers=auth_headers)
    assert r.status_code == 201, f"Failed to create contact: {r.text}"
    
    contact = r.json()
    contact_id = contact.get("_id")
    logger.info(f"Created contact with ID: {contact_id}")

    yield contact

    logger.info(f"Deleting contact: {contact_id}")
    delete_response = http_client.delete(f"/contacts/{contact_id}", headers=auth_headers)
    
    if delete_response.status_code != 200:
        logger.warning(
            f"Failed to delete contact {contact_id}. "
            f"Status: {delete_response.status_code}, "
            f"Response: {delete_response.text}"
        )


@pytest.fixture(scope="function")
def multiple_contacts(http_client, auth_headers):
    contacts = []
    count = 3
    
    for i in range(count):
        contact_data = {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "birthdate": faker.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
        "email": faker.email(),
        "phone": faker.numerify('800%%%%%%%'),
        "street1": faker.street_address(),
        "street2": faker.secondary_address(),
        "city": faker.city(),
        "stateProvince": faker.state_abbr(),
        "postalCode": faker.postcode(),
        "country": faker.country_code(representation="alpha-3")
    }
        
        response = http_client.post("/contacts", json=contact_data, headers=auth_headers)
        if response.status_code != 201:
            logger.error(f"Response text of failed request: {response.text}")
        assert response.status_code == 201, f"Failed to create contact #{i+1}"

        contacts.append(response.json())
    
    logger.info(f"Created {count} contacts for test")
    
    yield contacts
    
    for contact in contacts:
        contact_id = contact.get("_id")
        delete_response = http_client.delete(f"/contacts/{contact_id}", headers=auth_headers)
        
        if delete_response.status_code != 200:
            logger.warning(f"Failed to delete contact {contact_id}")