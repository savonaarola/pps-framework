from core.base_page import BasePage
from selenium.webdriver.common.by import By



class SteamMainPage(BasePage):
    ABOUT_BUTTON = (By.CSS_SELECTOR,"div.supernav_container a.menuitem[href*='https://store.steampowered.com/about/']")
    BROWSER_BUTTON = (By.CSS_SELECTOR, "div[role='navigation'] button:first-child")
    BROWSE_PANEL = (By.CSS_SELECTOR,"div.Panel[role='navigation'] + div")
    TOPSELLERS_LINK = (By.CSS_SELECTOR,"a[href*='https://store.steampowered.com/charts/topselling']")
    TOPSELLERS_H1 = (By.CSS_SELECTOR,"h1:first-child")
    TOPSELLERS_COUNTRY_CHOOSE_BUTTON = (By.CSS_SELECTOR,"h1:first-child + div")
    TOPSELLERS_COUNTRY_CHOOSE_GLOBAL = (By.CSS_SELECTOR,"div.DialogMenuPosition button:first-child")
    TOPSELLERS_ROWS = (By.CSS_SELECTOR,"tbody tr")

    TOPSELLERS_FIRST_GAME = (By.CSS_SELECTOR,"tr:first-child td > a")
    TOPSELLERS_FIRST_GAME_NAME = (By.CSS_SELECTOR,"tr:first-child td > a div")

    TOPSELLERS_GAME_NAME = (By.CSS_SELECTOR, "td > a div")
    TOPSELLERS_GAME_PRICE = (By.CSS_SELECTOR, "div.StoreSalePriceWidgetContainer")
    
    GAME_PAGE_GAME_NAME = (By.ID,"appHubAppName")

    def click_about_button(self):
        self.click(self.ABOUT_BUTTON)

    def click_browse_button(self):
        self.click(self.BROWSER_BUTTON)
        self.find_element(self.BROWSE_PANEL)
    
    def click_topsellers_link(self):
        self.click(self.TOPSELLERS_LINK)
        self.find_element(self.TOPSELLERS_H1)

    def click_topsellers_country_choose_button(self):
        self.click(self.TOPSELLERS_COUNTRY_CHOOSE_BUTTON)
        self.find_element(self.TOPSELLERS_COUNTRY_CHOOSE_GLOBAL)

    def click_topsellers_choose_global_country(self):
        self.click(self.TOPSELLERS_COUNTRY_CHOOSE_GLOBAL)

    def parse_topsellers_ten_games(self):
        games_data = {}
        rows = self.find_elements(self.TOPSELLERS_ROWS)
        for row in rows[:10]:
            try:
                name_elem = row.find_element(*self.TOPSELLERS_GAME_NAME)
                price_elem = row.find_element(*self.TOPSELLERS_GAME_PRICE)

                name = name_elem.text.strip()
                price = price_elem.text.strip().replace("\n", " ")

                if name:
                    games_data[name] = price if price else "N/A"


            except Exception:
                continue
        
        return games_data
    
    def get_first_topseller_name(self):
        return self.get_text(self.TOPSELLERS_FIRST_GAME_NAME)
    
    def click_first_topseller(self):
        self.click(self.TOPSELLERS_FIRST_GAME)
        self.find_element(self.GAME_PAGE_GAME_NAME)
    


class SteamGamePage(BasePage):
    GAME_NAME = (By.ID,"appHubAppName")
    RELEASE_DATE = (By.CSS_SELECTOR,"div.date")
    DEVELOPERS = (By.ID, "developers_list")

    def get_game_name(self):
        return self.get_text(self.GAME_NAME)
    
    def get_game_release_date(self):
        return self.get_text(self.RELEASE_DATE)
    
    def get_game_developers(self):
        return self.get_text(self.DEVELOPERS)
    


class SteamAboutPage(BasePage):
    ONLINE_PLAYERS_AMOUNT = (By.CSS_SELECTOR, "div.online_stat:nth-of-type(1)")
    INGAME_PLAYERS_AMOUNT = (By.CSS_SELECTOR, "div.online_stat:nth-of-type(2)")
    ABOUT_PAGE_URL_FRAGMENT = '/about/'
    
    def veify_page_loaded(self):
        self.verify_url_contains(self.ABOUT_PAGE_URL_FRAGMENT)

    def get_amount_players_online(self):
        return self.get_text(self.ONLINE_PLAYERS_AMOUNT)
    
    def get_amount_players_ingame(self):
        return self.get_text(self.INGAME_PLAYERS_AMOUNT)