from core.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AutomationPracticeFormPage(BasePage):

    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "userEmail")
    MALE_GENDER_INPUT = (By.CSS_SELECTOR, "input#gender-radio-1 + label")
    FEMALE_GENDER_INPUT = (By.CSS_SELECTOR, "input#gender-radio-2 + label")
    OTHER_GENDER_INPUT = (By.CSS_SELECTOR, "input#gender-radio-3 + label")
    MOBILE_INPUT = (By.ID, "userNumber")
    DATE_OF_BIRTH_INPUT = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    HOBBIES_SPORTS_INPUT = (By.CSS_SELECTOR, "input#hobbies-checkbox-1 + label")
    HOBBIES_READING_INPUT = (By.CSS_SELECTOR, "input#hobbies-checkbox-2 + label")
    HOBBIES_MUSIC_INPUT = (By.CSS_SELECTOR, "input#hobbies-checkbox-3 + label")
    UPLOAD_PICTURE_INPUT = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_INPUT = (By.ID, "currentAddress")
    STATE_DROPDOWN = (By.ID, "react-select-3-input")
    # NCR_SELECT_OPTION = (By.ID, "react-select-3-option-0")
    # UTTAR_PRADESH_SELECT_OPTION = (By.ID, "react-select-3-option-1")
    # HARYANA_SELECT_OPTION = (By.ID, "react-select-3-option-2")
    # RAJASTHAN_SELECT_OPTION = (By.ID, "react-select-3-option-3")
    CITY_DROPDOWN = (By.ID, "react-select-4-input")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button#submit")

    SUCCESS_MODAL = (By.ID, "example-modal-sizes-title-lg")
    MODAL_CLOSE_BUTTON = (By.ID, "closeLargeModal")
    
    def fill_name(self,name : str):
        self.find_element(self.FIRST_NAME_INPUT).send_keys(name)
    
    def fill_last_name(self,last_name : str):
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)

    def fill_email(self, email: str):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
    
    def select_gender(self, gender: str):
        if not gender:
            return
        gender_map = {
        "Male": self.MALE_GENDER_INPUT,
        "Female": self.FEMALE_GENDER_INPUT,
        "Other": self.OTHER_GENDER_INPUT
        }
        if gender in gender_map:
            self.click_js(gender_map[gender])
        else:
            raise ValueError(f"Invalid gender: {gender}")
        
    def fill_mobile(self, mobile: str):
        self.find_element(self.MOBILE_INPUT).send_keys(mobile)

    def fill_date_of_birth(self, date_of_birth: str):
        element = self.find_element(self.DATE_OF_BIRTH_INPUT)
        element.send_keys(Keys.CONTROL + "a")
        date_input = self.find_element(self.DATE_OF_BIRTH_INPUT)
        date_input.send_keys(date_of_birth)
        date_input.send_keys(Keys.ENTER)
        #self.find_element(self.SUBJECTS_INPUT).click()
    
    def fill_subjects(self, subject: str):
        self.find_element(self.SUBJECTS_INPUT).send_keys(subject)
        #self.find_element(self.SUBJECTS_INPUT).send_keys(Keys.ENTER)

    def select_hobbies(self, hobbies: list[str]):
        hobby_map = {
        "Sports": self.HOBBIES_SPORTS_INPUT,
        "Reading": self.HOBBIES_READING_INPUT,
        "Music": self.HOBBIES_MUSIC_INPUT
        }
        for hobby in hobbies:
            if hobby in hobby_map:
                self.click_js(hobby_map[hobby])
            else:
                raise ValueError(f"Invalid hobby: {hobby}")
            
    def upload_picture(self, file_path: str):
        import os
        absolute_path = os.path.abspath(file_path)
        self.find_element(self.UPLOAD_PICTURE_INPUT).send_keys(absolute_path)

    def fill_current_address(self, address: str):
        self.find_element(self.CURRENT_ADDRESS_INPUT).send_keys(address)
    
    def select_state(self, state: str):
        self.find_element(self.STATE_DROPDOWN).send_keys(state)
        self.find_element(self.STATE_DROPDOWN).send_keys(Keys.ENTER)
        self.to_be_clickable(self.CITY_DROPDOWN)

    def select_city(self, city: str):
        self.find_element(self.CITY_DROPDOWN).send_keys(city)
        self.find_element(self.CITY_DROPDOWN).send_keys(Keys.ENTER)

    def click_submit(self):

        self.click_js(self.SUBMIT_BUTTON)

            

    def fill_complete_form(self, form_data):
        if form_data.first_name:
            self.fill_name(form_data.first_name)

        if form_data.last_name:
            self.fill_last_name(form_data.last_name)

        if form_data.email:
            self.fill_email(form_data.email)
        
        if form_data.date_of_birth:
            self.fill_date_of_birth(form_data.date_of_birth)


        if form_data.gender:
            self.select_gender(form_data.gender)

        if form_data.mobile:
            self.fill_mobile(form_data.mobile)

        if form_data.hobbies:
            if form_data.hobbies:
                self.select_hobbies(form_data.hobbies)

        if form_data.subjects:
            if form_data.subjects:
                for subject in form_data.subjects:
                    self.fill_subjects(subject)



        if form_data.picture_path:
            self.upload_picture(form_data.picture_path)

        if form_data.address:
            self.fill_current_address(form_data.address)

        if form_data.state:
            self.select_state(form_data.state)

        if form_data.city:
            self.select_city(form_data.city)

    def is_form_submitted(self, timeout = 5) -> bool:
        try:
            self.find_element(self.SUCCESS_MODAL, timeout=timeout)
            return True
        except:
            return False
        
    def is_field_invalid(self, locator, timeout=5) -> bool:
        try:
            import time
            element = self.find_element(locator, timeout=timeout)
            
            end_time = time.time() + timeout
            while time.time() < end_time:
                border_color = element.value_of_css_property("border-color")
                is_red_border = "rgb(220, 53, 69)" in border_color or "rgb(255, 0, 0)" in border_color
                if is_red_border:
                    return True
                time.sleep(0.2)
            
            return False
        except:
            return False
        
    