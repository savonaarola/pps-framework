from core.base_page import BasePage
from selenium.webdriver.common.by import By



class SteamMainPage(BasePage):
    ABOUT_BUTTON = (By.CSS_SELECTOR,"div.supernav_container a.menuitem[href*='https://store.steampowered.com/about/']")

    def click_about_button(self):
        self.click(self.ABOUT_BUTTON)


class SteamAboutPage(BasePage):
    ONLINE_PLAYERS_AMOUNT = (By.CSS_SELECTOR, "div.online_stat_label.gamers_online")
    INGAME_PLAYERS_AMOUNT = (By.CSS_SELECTOR, "div.online_stat_label.gamers_in_game")

    def get_amount_players_online(self):
        return self.get_text(self.ONLINE_PLAYERS_AMOUNT)
    
    def get_amount_players_online(self):
        return self.get_text(self.INGAME_PLAYERS_AMOUNT)