from common_files.recipe_handler import Recipe
from selenium import webdriver
import re
import string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
PATH = r"C:\\Users\\punee\\Downloads\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(PATH, chrome_options=options)
# driver=webdriver.Chrome(PATH)
original_categories_handle = ''
original_recipes_handle = ''


recipe_meal_type = Recipe.MealType("any time", "any part")
recipe = Recipe("any title", recipe_meal_type)
print(recipe.meal_type.part_of_meal)

current_category = ""


def process_recipe_page(url):
    script = "window.open('{0}', 'recipe_window')".format(url)
    driver.execute_script(script)
    original_recipes_handle = driver.window_handles[-2]
    driver.switch_to.window(driver.window_handles[-1])
    recipe_title = driver.find_element(By.XPATH,"//h1").text
    print("Title: {}".format(recipe_title))
    try:
        recipe_alt_title=driver.find_element(By.XPATH,"//h2").text
        print("Alt Title: {}".format(recipe_alt_title))
    except:
        pass
    
    driver.close()
    driver.switch_to.window(original_recipes_handle)

def process_category_page(url):
    script = "window.open('{0}', 'category_window')".format(url)
    driver.execute_script(script)
    original_categories_handle = driver.window_handles[-2]
    driver.switch_to.window(driver.window_handles[-1])
    current_category=driver.find_element(By.XPATH,"""//h1""").text
    view_all_button = driver.find_element(
        By.XPATH, """//*[contains(concat( " ", @class, " " ), concat( " ", "view-all", " " ))]""").click()

    recipe_tiles = driver.find_elements(
        By.XPATH, """//*[contains(concat( " ", @class, " " ), concat( " ", "tile", " " ))]""")
    for recipe_tile in recipe_tiles:
        recipe_tile_article = recipe_tile.find_element(
            By.XPATH, """article/a""")
        recipe_url = recipe_tile_article.get_attribute("href")
        # print(recipe_url)
        process_recipe_page(recipe_url)
    driver.close()
    driver.switch_to.window(original_categories_handle)


page_url = "https://www.harighotra.co.uk/indian-recipes/courses"
driver.get(page_url)
driver.maximize_window()
categories = driver.find_elements(
    By.XPATH, """//*[contains(concat( " ", @class, " " ), concat( " ", "category", " " ))]""")

# print(len)
for category in categories:
    article = category.find_element(By.XPATH, """article/a""")
    category_url = article.get_attribute("href")
    process_category_page(category_url)
