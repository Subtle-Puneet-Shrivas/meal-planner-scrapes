import math
import re
import spacy
nlp = spacy.load('en_core_web_sm')


class Recipe:
    def __init__(self, recipe_title, meal_type):
        self.title = recipe_title
        self.ingredients = []
        self.steps = []
        self.resources = []
        self.metas=[]
        self.nutrition_values=[]
        self.meal_type=meal_type
        self.media_contents=[]


    class Ingredient:
        def __init__(self, ingredient_id, name, quantity):
            self.id = ingredient_id
            self.name = name
            self.quantity = quantity

    class Step:
        def __init__(self, instruction, phase, time, triggers, ingredients, resources):
            self.media_contents = []
            self.instruction = instruction
            self.phase = phase
            self.time = time
            self.triggers = triggers
            self.ingredients = ingredients
            self.resources = resources

    class Resource:
        def __init__(self, utensil, tool):
            self.utensil = utensil
            self.tool = tool

    class Meta:
        def __init__(self, cuisine, time_to_cook, nutritional_values, ratings, meal_type, regional_info, description):
            self.cuisine = cuisine
            self.time_to_cook = time_to_cook
            self.nutritional_values = nutritional_values
            self.ratings = ratings
            self.meal_type = meal_type
            self.regional_info = regional_info
            self.description = description


    class NutritionalValue:
        def __init__(self, name, value):
            self.name = name
            self.value = value


    class MealType:
        def __init__(self, time_of_day, part_of_meal):
            self.time_of_day = time_of_day
            self.part_of_meal = part_of_meal


    class MediaContent:
        def __init__(self, resource_title, url):
            self.resource_title = resource_title
            self.url = url