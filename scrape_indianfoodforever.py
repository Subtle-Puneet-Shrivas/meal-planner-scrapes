from common_files.recipe_handler import Recipe
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from common_files.utils import WebScrapper


page_url = "https://www.indianfoodforever.com/"
chrome_options = Options()
chrome_options.binary_location = os.environ['BRAVE_PATH']
chrome_options.add_experimental_option("detach", True)
executable_path = os.environ['CHROME_DRIVER_PATH']

scrapper = WebScrapper(
    get_url=page_url, executable_path=executable_path, options=chrome_options)

scrapper.startDriver()

res = scrapper.recurringAttributeScrapper(parent_item_options={'xpath': '//*[(@id = "menu-pri-menu-in-header")]//a', 'attributes': ["href"]}, child_item_options={
    'xpath': '//*[contains(concat( " ", @class, " " ), concat( " ", "entry-title", " " ))]//a', 'attributes': ["href"]})

for link in res['href']:
    print(link)
