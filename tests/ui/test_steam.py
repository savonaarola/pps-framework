from pages.steam_page import SteamAboutPage,SteamMainPage
import pytest


@pytest.mark.ui
def test_compare_amount_online_vs_ingame(driver):
    driver.get('https://store.steampowered.com/')
    main_page = SteamMainPage(driver)
    main_page.click_about_button()
    
    about_page = SteamAboutPage(driver)
    about_page.veify_page_loaded()
    online_amount = about_page.get_amount_players_online()
    ingame_amount = about_page.get_amount_players_ingame()
    
    assert online_amount > ingame_amount