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
options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
PATH=r"C:\\Users\\punee\\Downloads\\chromedriver_win32\\chromedriver.exe"
# driver = webdriver.Chrome(PATH,chrome_options=options)
driver=webdriver.Chrome(PATH)

from common_files.recipe_handler import Recipe
recipe_meal_type=Recipe.MealType("any time","any part")
recipe=Recipe("any title",recipe_meal_type)
print(recipe.meal_type.part_of_meal)

page_url="https://www.harighotra.co.uk/indian-recipes"
driver.get(page_url)
driver.maximize_window()
categories=driver.find_elements(By.XPATH,"""//*[contains(concat( " ", @class, " " ), concat( " ", "category-title", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]""")
print(len)
for category in categories:
    print(category.text)