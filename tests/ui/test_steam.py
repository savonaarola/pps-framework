from pages.steam_page import SteamAboutPage,SteamMainPage,SteamGamePage
import pytest
from core.logger import logging

logger = logging.getLogger(__name__)

@pytest.mark.ui
def test_compare_amount_online_vs_ingame(driver):
    driver.get('https://store.steampowered.com/')
    main_page = SteamMainPage(driver)
    main_page.click_about_button()
    
    about_page = SteamAboutPage(driver)
    about_page.veify_page_loaded()
    online_amount = about_page.get_amount_players_online()
    ingame_amount = about_page.get_amount_players_ingame()
    logger.info(f"Players online: {online_amount}, Players in-game: {ingame_amount}")
    assert online_amount > ingame_amount


@pytest.mark.ui
def test_parse_top_ten_sellers(driver):
    driver.get('https://store.steampowered.com/')
    main_page=SteamMainPage(driver)
    main_page.click_browse_button()
    main_page.click_topsellers_link()
    main_page.click_topsellers_country_choose_button()
    main_page.click_topsellers_choose_global_country()
    games_data = main_page.parse_topsellers_ten_games()
    
    assert games_data, f"Ожидалось 10, получено: {len(games_data)}"

    for name, price in games_data.items():
        print(f"{name:<40} | {price}")


@pytest.mark.ui
def test_check_top_seller(driver):
    driver.get('https://store.steampowered.com/')
    main_page=SteamMainPage(driver)
    main_page.click_browse_button()
    main_page.click_topsellers_link()
    main_page.click_topsellers_country_choose_button()
    main_page.click_topsellers_choose_global_country()
    topseller_name = main_page.get_first_topseller_name()
    main_page.click_first_topseller()
    game_page = SteamGamePage(driver)
    game_name = game_page.get_game_name()

    assert topseller_name == game_name

    logger.info(f"Game name: {game_name}")
    logger.info(f"Game release date: {game_page.get_game_release_date()}")
    logger.info(f"Game developers: {game_page.get_game_developers()}")
    