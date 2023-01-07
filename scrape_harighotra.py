import spacy
from common_files.recipe_handler import Recipe, parameterize_ingredient_phrase, ComplexEncoder
from common_files.mogodb_functions import postRecipe
from common_files.s3_functions import upload_image_to_s3
from selenium import webdriver
import re
import requests
from PIL import Image
from io import StringIO
from datetime import datetime, timedelta
import json
import time
import os
from json_tricks import dump, dumps, load, loads, strip_comments
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urlparse, parse_qs


def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
PATH = r"C:\\Users\\punee\\Downloads\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(PATH, chrome_options=options)
# driver=webdriver.Chrome(PATH)
original_categories_handle = ''
original_recipes_handle = ''

nlp = spacy.load('en_core_web_sm')

# recipe_meal_type = Recipe.MealType("any time", "any part")
# recipe = Recipe("any title", recipe_meal_type)
# print(recipe.meal_type.part_of_meal)

current_cuisine = ""
current_meal_type = ""


def process_recipe_page(url):
    # Switching windows
    script = "window.open('{0}', 'recipe_window')".format(url)
    driver.execute_script(script)
    original_recipes_handle = driver.window_handles[-2]
    driver.switch_to.window(driver.window_handles[-1])
    try:
        # Recipe Title and Alternate Titles
        recipe_title = driver.find_element(By.XPATH, "//h1").text
        print("Title: {}".format(recipe_title))
        try:
            recipe_alt_title = driver.find_element(By.XPATH, "//h2").text
            print("Alt Title: {}".format(recipe_alt_title))
        except:
            recipe_alt_title = ""
        recipe = Recipe(recipe_title, recipe_alt_title)

        # Recipe one liner description
        try:
            description_one_liner = driver.find_element(
                By.XPATH, """//*[contains(concat( " ", @class, " " ), concat( " ", "intro", " " ))]//h3""").text
        except:
            description_one_liner = ""

        # Recipe description paragraphs
        description_paragraphs = []
        description_sections = driver.find_elements(
            By.XPATH, """//*[contains(concat( " ", @class, " " ), concat( " ", "desc", " " ))]//p""")
        for description_section in description_sections:
            sentences = [i.text for i in nlp(description_section.text).sents]
            description_paragraphs.append(sentences)
        # print(description_paragraphs)
        recipe_description = Recipe.Description(
            description_one_liner, description_paragraphs)
        # print(recipe_description)

        # Recipe ingredients
        recipe_ingredients = []
        ingredient_sections = driver.find_elements(
            By.XPATH, """//*[(@id = "js-content")]//li""")
        for ingredient_section in ingredient_sections:
            if(len(ingredient_section.text) > 0):
                ingredient_parameters = parameterize_ingredient_phrase(
                    ingredient_section.text)
                # print("ingredient statement: {}".format(ingredient_section.text))
                # print("len: {}".format(len(ingredient_section.text)))
                ingredient_id = ""
                ingredient_object = Recipe.Ingredient(
                    ingredient_id, ingredient_parameters[0], ingredient_parameters[1], ingredient_parameters[2], ingredient_parameters[3])
                recipe_ingredients.append(ingredient_object)

        # Recipe steps
        recipe_steps = []
        method_button = driver.find_element(
            By.XPATH, """/html/body/div[3]/div[3]/div[1]/div[1]/div[6]/ul/li[2]""").click()
        method_sections = driver.find_elements(
            By.XPATH, """//*[(@id = "js-content")]//li""")
        for method_section in method_sections:
            instruction = method_section.text
            # TODO add functions for parsing remaining step information
            # print(instruction)
            if(len(instruction) > 0):
                # print("step statement: {}".format(instruction))
                # print("len: {}".format(len(instruction)))
                step_object = Recipe.Step(
                    instruction, "", timedelta(minutes=10), "", "", "")
                recipe_steps.append(step_object)

        # Recipe metas
        info_section_handles = driver.find_elements(
            By.XPATH, """//*[contains(concat( " ", @class, " " ), concat( " ", "info", " " ))]""")
        info_section_text = []
        dietary_info = []
        for info_section_handle in info_section_handles:
            info_section_text.append(info_section_handle.text)
        texts = info_section_text[0].split()
        for i, text in enumerate(texts):
            if(text == "HEAT"):
                heat = texts[i+1]
            if(text == "SERVES"):
                serves = texts[i+1]
            if(text == "PREP"):
                prep_time = texts[i+1]
            if(text == "COOK"):
                cook_time = texts[i+1]
            if(text == "DIETARY"):
                n = 2
                while((i+n) < len(texts)):
                    if(texts[i+n] == "PREP"):
                        break
                    else:
                        dietary_info.append(texts[i+n])
                    n = n+1
        # print(dietary_info)

        # try:
        #     print("heat: ", heat)
        # except:
        #     pass
        # try:
        #     print("serves: ", serves)
        # except:
        #     pass
        # try:
        #     print("dietary infos: ", dietary_info)
        # except:
        #     pass
        # try:
        #     print("prep_time: ", prep_time)
        # except:
        #     pass
        # try:
        #     print("cook_time: ", cook_time)
        # except:
        #     pass

        # Nutrition values
        nutritional_value_sections = driver.find_elements(By.XPATH, """//td""")
        params = []
        units = []
        values = []
        #TODO correct order of values
        for nutritional_value_section in nutritional_value_sections:
            # print(nutritional_value_section.text)
            if(nutritional_value_section.text.replace(".", "", 1).isnumeric()):
                values.append(nutritional_value_section.text)
            else:
                unit_found = ""
                try:
                    unit_found = (re.search(
                        '\(([^)]+)', nutritional_value_section.text).group(0).replace("(", ""))
                except:
                    pass
                units.append(unit_found)
                params.append(nutritional_value_section.text.replace(unit_found, "").replace(
                    "(", "").replace(")", "").replace("of which", ""))
        nutritional_values = []
        for i in range(len(params)):
            nutritional_values.append({"param":params[i], "unit":units[i], "value":values[i]})
        # print(nutritional_values)
        recipe_metas = Recipe.Meta(
            current_cuisine, cook_time, prep_time, nutritional_values, dietary_info, 0.0, current_meal_type, "")
        
        
        #Get recipe images
        resource_title=""
        # i_url = ""
        try:
            try:
                image_url = driver.find_element(By.XPATH,"""//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-8", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "loaded", " " ))]""").get_attribute("src")
            except:
                image_url = driver.find_element(By.XPATH,"""/html/body/div[3]/div[3]/div[1]/div[1]/div[3]/picture/img""")
            resource_title="img"
        except:
            # youtube_section = driver.find_element(By.XPATH,"""/html/body/div[1]/div/div[4]/div""").value_of_css_property("backround-image")
            try:
                # youtube_section = driver.find_element(By.XPATH,"""//*[contains(concat( " ", @class, " " ), concat( " ", "iframe-wrap", " " ))]//iframe""").value_of_css_property("backround-image")
                iframe_obj=driver.find_element(By.XPATH,"""/html/body/div[3]/div[3]/div[1]/div[1]/div[3]/div/iframe""").get_attribute("src")
                image_url="""https://i.ytimg.com/vi_webp/{}/maxresdefault.webp""".format(get_id(iframe_obj))
            except:
                youtube_section = driver.find_element(By.XPATH,"""/html/body/div/div/div[4]/div""").value_of_css_property("backround-image")
            resource_title="yt_thumb"
            # image_url =re.split('[()]',youtube_section)[1]
        r = requests.get(image_url).content
        image_name = recipe_title.replace(" ","_") + "_" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
        with open (image_name, 'wb') as f:
            f.write(r)
        upload_image_to_s3(image_name,image_name) #stores image in s3
        print(image_name)
        os.remove(image_name)
        recipe_media_contents = Recipe.MediaContent(resource_title,image_name)

        # Create object
        recipe_object = Recipe(recipe_title, recipe_alt_title)
        recipe_object.description = recipe_description
        recipe_object.ingredients = recipe_ingredients
        recipe_object.steps = recipe_steps
        recipe_object.metas = recipe_metas
        recipe_object.media_contents = recipe_media_contents

        # print(dumps(recipe_object,primitives=True, indent=4))
        print(postRecipe(json.loads(dumps(recipe_object,primitives=True,indent=4)))) #Stores objects in mongodb
        

    except:
        print("failed url:",url)
    driver.close()
    driver.switch_to.window(original_recipes_handle)


def process_category_page(url):
    script = "window.open('{0}', 'category_window')".format(url)
    driver.execute_script(script)
    original_categories_handle = driver.window_handles[-2]
    driver.switch_to.window(driver.window_handles[-1])
    current_category = driver.find_element(By.XPATH, """//h1""").text.split()
    current_cuisine = current_category[0]
    current_meal_type = current_category[1]
    print("current_cuisine: {}".format(current_cuisine))
    print("current_meal_type: {}".format(current_meal_type))


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

for category in categories:
    article = category.find_element(By.XPATH, """article/a""")
    category_url = article.get_attribute("href")
    process_category_page(category_url)
