import pytest
from pages.demoqa_page import AutomationPracticeFormPage
from test_data.demoqa_form_data import * 



@pytest.mark.ui
@pytest.mark.positive
def test_fill_form_correct(driver):
    driver.get('https://demoqa.com/automation-practice-form')
    form_page = AutomationPracticeFormPage(driver)
    form_data = create_valid_form_data()
    form_page.fill_complete_form(form_data)
    form_page.click_submit()
    assert form_page.is_form_submitted(), "Форма не была успешно отправлена"

@pytest.mark.ui
@pytest.mark.positive
def test_fill_form_with_picture(driver):
    driver.get('https://demoqa.com/automation-practice-form')
    form_page = AutomationPracticeFormPage(driver)
    form_data = create_valid_form_data(picture_path='test_data/files/chupep.jpg')
    form_page.fill_complete_form(form_data)
    form_page.click_submit()
    assert form_page.is_form_submitted(), "Форма не была успешно отправлена"

@pytest.mark.ui
@pytest.mark.negative
def test_fill_form_invalid_email(driver):
    driver.get('https://demoqa.com/automation-practice-form')
    form_page = AutomationPracticeFormPage(driver)
    form_data = create_invalid_email_data()
    form_page.fill_complete_form(form_data)
    form_page.click_submit()
    assert form_page.is_field_invalid(form_page.EMAIL_INPUT), "Поле Email не помечено как некорректное"

@pytest.mark.ui
@pytest.mark.negative
def test_fill_form_invalid_mobile(driver):
    driver.get('https://demoqa.com/automation-practice-form')
    form_page = AutomationPracticeFormPage(driver)
    form_data = create_invalid_mobile_data()
    form_page.fill_complete_form(form_data)
    form_page.click_submit()
    assert form_page.is_field_invalid(form_page.MOBILE_INPUT), "Поле Mobile не помечено как некорректное"

@pytest.mark.ui
@pytest.mark.negative
def test_fill_form_no_gender(driver):
    driver.get('https://demoqa.com/automation-practice-form')
    form_page = AutomationPracticeFormPage(driver)
    form_data = create_missing_gender_data()
    form_page.fill_complete_form(form_data)
    form_page.click_submit()
    assert form_page.is_field_invalid(form_page.MALE_GENDER_INPUT), "Поле Gender не помечено как некорректное"

@pytest.mark.ui
@pytest.mark.negative
def test_fill_form_empty(driver):
    driver.get('https://demoqa.com/automation-practice-form')
    form_page = AutomationPracticeFormPage(driver)
    form_data = create_empty_form_data()
    form_page.fill_complete_form(form_data)
    form_page.click_submit()
    assert form_page.is_field_invalid(form_page.FIRST_NAME_INPUT), "Поле First Name не помечено как некорректное"
    assert form_page.is_field_invalid(form_page.LAST_NAME_INPUT), "Поле Last Name не помечено как некорректное"
    assert form_page.is_field_invalid(form_page.MALE_GENDER_INPUT), "Поле Gender не помечено как некорректное"
    assert form_page.is_field_invalid(form_page.MOBILE_INPUT), "Поле Mobile не помечено как некорректное"