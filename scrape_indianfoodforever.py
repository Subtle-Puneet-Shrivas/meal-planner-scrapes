from common_files.recipe_handler import Recipe
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

page_url = "https://www.indianfoodforever.com/"
options = Options()
options.binary_location = os.environ['BRAVE_PATH']
driver = webdriver.Chrome(
    os.environ['CHROME_DRIVER_PATH'], options=options)

recipe_meal_type = Recipe.MealType("any time", "any part")
recipe = Recipe("any title", recipe_meal_type)

driver.get(page_url)
