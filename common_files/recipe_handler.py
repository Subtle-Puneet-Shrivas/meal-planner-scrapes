from enum import Enum
import spacy
from datetime import datetime, timedelta
import typing as _type
nlp = spacy.load('en_core_web_sm')


class MealTime(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SUPPER = 4
    BRUNCH = 5


class MealPart(Enum):
    SOUP = 1
    APPETIZER = 1
    SALAD = 1
    MAIN_COURSE = 1
    DESSERT = 1


class NutritionParam(Enum):
    CALORIES = 1
    PROTEIN = 2
    FAT_TOTAL = 3
    FAT_MONO_UNSATURATED = 4
    FAT_POLY_UNSATURATED = 5


class Unit(Enum):
    UNIT = 0
    KCAL = 1
    GRAM = 2
    PERCENTAGE = 3
    KILOGRAM = 4


class NutritionType:
    '''Defines type of nutrition - 
eg. NutritionType(param=NutritionParam.PROTIEN, value=50, unit=Unit.GRAM)
    '''

    def __init__(self, param: NutritionParam, value: int, unit: Unit):
        self.param = param
        self.value = value
        self.unit = unit


class TimeType:
    def __init__(self, value: int, unit: Unit):
        self.value = value
        self.unit = unit

class MealType:
    def __init__(self, meal_time: MealTime, meal_part: MealPart):
        self.meal_time = meal_time
        self.meal_part = meal_part


class Recipe:
    def __init__(self, recipe_title, alternate_title=""):
        self.title = recipe_title
        self.alternate_title = alternate_title
        self.ingredients = []
        self.steps = []
        self.metas = []
        self.media_contents = []

    class Ingredient:
        def __init__(self, ingredient_id, name, quantity: float, unit: Unit, prep_hint: str):
            self.id = ingredient_id
            self.name = name
            self.quantity = quantity
            self.quantity_unit = unit
            self.prep_hint = prep_hint

    class Step:
        def __init__(self, instruction, phase, time: timedelta, triggers, ingredients, resources):
            self.media_contents = []
            self.instruction = instruction
            self.phase = phase
            self.time = time
            self.triggers = triggers
            self.ingredients = ingredients
            self.resources = resources

    class Meta:
        def __init__(self, cuisine: str, time_to_cook: timedelta, nutritional_values: _type.List[NutritionType], ratings: float, meal_type: MealType, regional_info, description):
            self.cuisine = cuisine
            self.time_to_cook = time_to_cook
            self.nutritional_values = nutritional_values
            self.ratings = ratings
            self.meal_type = meal_type
            self.regional_info = regional_info
            self.description = description

    class MediaContent:
        def __init__(self, resource_title: str, url: str):
            self.resource_title = resource_title
            self.url = url

def parameterize_ingredient_phrase(phrase):
    name=""
    quantity = ""
    quantity_unit= ""
    prep_hint = ""
    return [name, quantity, quantity_unit, prep_hint]
