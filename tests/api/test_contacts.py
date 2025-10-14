import pytest 
from faker import Faker
from core.logger import logging
import allure 

logger = logger = logging.getLogger(__name__)
faker = Faker()

@allure.epic("Contact List API")
@allure.feature("Contacts")
@allure.title("User can get contact by id")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.smoke
def test_get_contact_by_id(http_client, auth_headers, new_contact):
    contact_id = new_contact.get("_id")
    r = http_client.get(f"/contacts/{contact_id}",headers=auth_headers)
    assert r.status_code == 200
    contact = r.json()
    assert contact.get("firstName") == new_contact.get("firstName")
    allure.attach(
        f"Contact ID: {contact.get('_id')}\n"
        f"Name: {contact.get('firstName')} {contact.get('lastName')}\n"
        f"Email: {contact.get('email')}\n"
        f"Phone: {contact.get('phone', 'N/A')}\n"
        f"City: {contact.get('city', 'N/A')}",
        name="Retrieved Contact",
        attachment_type=allure.attachment_type.TEXT
    )



@allure.epic("Contact List API")
@allure.feature("Contacts")
@allure.title("User can get list of contacts")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.smoke
def test_get_contacts_list(http_client, auth_headers, multiple_contacts):

    response = http_client.get("/contacts", headers=auth_headers)
    
    assert response.status_code == 200
    
    contacts = response.json()
    
    assert len(contacts) == len(multiple_contacts)

    contacts_info = f"Total contacts: {len(contacts)}\n"
    
    for idx, contact in enumerate(contacts, start=1):
        contacts_info += (
            f"{idx}. {contact.get('firstName')} {contact.get('lastName')} "
            f"(ID: {contact.get('_id')})\n"
            f"   Email: {contact.get('email')}\n"
        )
    
    allure.attach(
        contacts_info,
        name="Contacts List",
        attachment_type=allure.attachment_type.TEXT
    )




@allure.epic("Contact List API")
@allure.feature("Contacts")
@allure.title("User can add another contact to his list")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.smoke
def test_add_contact_to_list_of_contacts(http_client, auth_headers, multiple_contacts, contact_data):
    r = http_client.post("/contacts", headers=auth_headers,json=contact_data)
    assert r.status_code == 201

    rv = http_client.get("/contacts", headers=auth_headers)
    assert rv.status_code == 200
    assert len(rv.json()) == len(multiple_contacts)+1
    allure.attach(
        f"Added new contact {contact_data.get("firstName")} {contact_data.get("lastName")} to the list",
        name="Adding new contact",
        attachment_type=allure.attachment_type.TEXT
    )



@allure.epic("Contact List API")
@allure.feature("Contacts")
@allure.title("User can change some field in particular contact")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
def test_patch_contact(http_client, auth_headers, new_contact):
    contact_id = new_contact.get("_id")
    original_email = new_contact.get("email")
    original_lastname = new_contact.get("lastName")
    
    update_data = {
        "firstName": faker.first_name() + "Patched",
        "phone": faker.numerify('800%%%%%%%')
    }
    
    logger.info(f"PATCH updating contact {contact_id}: {update_data}")
    

    response = http_client.patch(f"/contacts/{contact_id}", json=update_data, headers=auth_headers)
    
    assert response.status_code == 200
    
    updated_contact = response.json()
    

    assert updated_contact.get("firstName") == update_data["firstName"]
    assert updated_contact.get("phone") == update_data["phone"]
    

    assert updated_contact.get("email") == original_email
    assert updated_contact.get("lastName") == original_lastname
    
    logger.info(f"Contact {contact_id} successfully updated with PATCH")
    

    allure.attach(
        f"Updated fields:\n{update_data}\n\nOriginal email preserved: {original_email}",
        name="Update Details",
        attachment_type=allure.attachment_type.TEXT
    )





@allure.epic("Contact List API")
@allure.feature("Contacts")
@allure.title("User can replace some contact with another")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
def test_put_contact(http_client, auth_headers, new_contact):
    
    contact_id = new_contact.get("_id")
    original_firstname = new_contact.get("firstName")
    
    new_contact_data = {
        "firstName": "ReplacedFirstName",   
        "lastName": "ReplacedLastName",       
        "email": faker.email(),                
        "phone": faker.numerify('800%%%%%%%'),          
        "birthdate": "1990-01-01",             
        "street1": "123 Replaced St",
        "street2": "Apt R",
        "city": "ReplacedCity",
        "stateProvince": "CA",
        "postalCode": "90210",
        "country": "USA"
    }
    
    logger.info(f"PUT replacing contact {contact_id} with new data")
    logger.info(f"Original firstName: {original_firstname}")
    logger.info(f"New firstName: {new_contact_data['firstName']}")
    

    response = http_client.put(f"/contacts/{contact_id}",json=new_contact_data,headers=auth_headers)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    replaced_contact = response.json()
    
    assert replaced_contact.get("_id") == contact_id, "Contact ID should not change"
    

    assert replaced_contact.get("firstName") == new_contact_data["firstName"]
    assert replaced_contact.get("lastName") == new_contact_data["lastName"]
    assert replaced_contact.get("email") == new_contact_data["email"]
    assert replaced_contact.get("phone") == new_contact_data["phone"]
    assert replaced_contact.get("city") == new_contact_data["city"]
    assert replaced_contact.get("firstName") != original_firstname
    
    logger.info(f"Contact {contact_id} successfully replaced with PUT")
    
    allure.attach(
        f"Original firstName: {original_firstname}\n"
        f"New firstName: {replaced_contact.get('firstName')}\n"
        f"All fields replaced",
        name="Replacement Details",
        attachment_type=allure.attachment_type.TEXT
    )


@allure.epic("Contact List API")
@allure.feature("Contacts")
@allure.title("User can delete contact by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.smoke
def test_delete_contact(http_client, auth_headers, new_contact):
    contact_id = new_contact.get("_id")
    contact_name = f"{new_contact.get('firstName')} {new_contact.get('lastName')}"
    
    logger.info(f"Deleting contact {contact_id}: {contact_name}")
    
    delete_response = http_client.delete(f"/contacts/{contact_id}",headers=auth_headers)

    assert delete_response.status_code == 200
    
    logger.info(f"Contact {contact_id} deleted successfully")
    
    get_response = http_client.get(f"/contacts/{contact_id}", headers=auth_headers)
    assert get_response.status_code == 404

    logger.info(f"Verified: contact {contact_id} no longer exists (404)")

    allure.attach(
        f"Deleted contact ID: {contact_id}\n"
        f"Contact name: {contact_name}\n"
        f"Verification: GET request returned 404",
        name="Deletion Details",
        attachment_type=allure.attachment_type.TEXT
    )