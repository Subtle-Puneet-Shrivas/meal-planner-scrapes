from enum import Enum
import spacy
from datetime import datetime, timedelta
import typing as _type
import re
nlp = spacy.load('en_core_web_sm')

quantity_pos = ["NUM"]
quantity_tag = ["CD"]
quantity_identifiers = ["¼","½","¾","⅓","⅔","⅕","⅖","⅗","⅘","⅙","⅚","⅛","⅜","⅝","⅞"]
quantity_unit_identifiers = ["g","gms","grams","l","litres","ml","mL","L","dl","dL","teaspoon","tablespoon","cup","pint","quart","quarters","gallon","mg","pound","ounce","mm","cm","mililitres","kg","kilograms","tsp","tbsp"]


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


def get_quantity_identifier_regexp(quantity_identifiers):
    re_quantity_identifier_str = '\w*[' + ''.join(quantity_identifiers) + ']\w*'
    quantity_identifier_regexp = '('+re_quantity_identifier_str+')'
    return quantity_identifier_regexp

def get_quantity_unit_identifier_regexp(quantity_unit_identifiers):
    re_quantity_unit_identifier_str = '(' + '|'.join(quantity_unit_identifiers) + ')'
    quantity_unit_identifier_regexp = re_quantity_unit_identifier_str
    return quantity_unit_identifier_regexp

def parameterize_ingredient_phrase(phrase):
    # TODO add ingredient name and prep hint segregator
    quantity_identifier_regexp = get_quantity_identifier_regexp(quantity_identifiers)
    quantity_unit_identifier_regexp = get_quantity_unit_identifier_regexp(quantity_unit_identifiers)
    name = []
    quantity = []
    quantity_unit = []
    prep_hint = []
    doc = nlp(phrase)
    deleted_tokens=[]
    for token in doc:
        if((token.pos_ in quantity_pos) or (token.tag_ in quantity_tag) or (re.fullmatch(quantity_identifier_regexp, token.text))):
            quantity.append(token.text)
            # phrase = phrase[:token.idx]+phrase[token.idx + len(token.text):]
            deleted_tokens.append(token.i)
        elif(re.fullmatch(quantity_unit_identifier_regexp, token.text)):
            quantity_unit.append(token.text)
            # phrase = phrase[:token.idx]+phrase[token.idx + len(token.text):]
            deleted_tokens.append(token.i)
    remaining_phrase = []
    for token in doc:
        if token.i not in deleted_tokens:
            remaining_phrase.append(token.text + " ")
    doc= nlp("".join(remaining_phrase))
    # print("Remaining Phrase: {}".format("".join(remaining_phrase)))
    return [name, quantity, quantity_unit, prep_hint]
