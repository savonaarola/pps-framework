"""Test data and factories for DemoQA Automation Practice Form"""

from dataclasses import dataclass
from typing import Optional, List
from faker import Faker


@dataclass
class FormData:
    first_name: str
    last_name: str
    email: str
    gender: str
    mobile: str
    date_of_birth: str
    subjects: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None
    picture_path: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None


fake = Faker('ru_RU')


def create_valid_form_data(**overrides):

    default_data = {
        'first_name': fake.first_name(),     
        'last_name': fake.last_name(),
        'email': fake.email(),
        'gender': fake.random_element(['Male', 'Female', 'Other']),
        'mobile': fake.numerify('##########'),  
        'date_of_birth': '15 Jan 1990',
        'subjects': ['Maths'],
        'hobbies': ['Sports'],
        'address': fake.address().replace('\n', ', '), 
        'state': 'NCR',
        'city': 'Delhi'
    }
    default_data.update(overrides)
    return FormData(**default_data)


def create_invalid_email_data(**overrides):
    return create_valid_form_data(email='invalid_email@', **overrides)


def create_invalid_mobile_data(**overrides):
    return create_valid_form_data(mobile='123', **overrides)


def create_missing_gender_data(**overrides):
    return create_valid_form_data(gender='', **overrides)


def create_empty_form_data():
    return FormData(
        first_name='',
        last_name='',
        email='',
        gender='',
        mobile='',
        date_of_birth='',
        subjects=None,
        hobbies=None,
        address='',
        state='',
        city=''
    )


EDGE_CASE_LONG_NAME = FormData(
    first_name='A' * 255, 
    last_name='B' * 255,
    email='test@example.com',
    gender='Male',
    mobile='1234567890',
    date_of_birth='01 Jan 2000'
)

EDGE_CASE_SPECIAL_CHARS = FormData(
    first_name="O'Neill",
    last_name='Müller',
    email='test+tag@example.com',
    gender='Female',
    mobile='9876543210',
    date_of_birth='31 Dec 1999'
)
