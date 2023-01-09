from enum import Enum
import spacy
import json
from datetime import datetime, timedelta
import typing as _type
import re
nlp = spacy.load('en_core_web_sm')

quantity_pos = ["NUM"]
quantity_tag = ["CD"]
quantity_identifiers = ["¼", "½", "¾", "⅓", "⅔",
                        "⅕", "⅖", "⅗", "⅘", "⅙", "⅚", "⅛", "⅜", "⅝", "⅞", "\d+\/\d+"]
quantity_unit_identifiers = ["g", "gms", "grams", "l", "litres", "ml", "mL", "L", "dl", "dL", "teaspoon", "tablespoon", "cup", "pinch", "pinche", "piece", "pieces", "pinches", "handful",
                             "pint", "quart", "quarters", "gallon", "mg", "pound", "ounce", "mm", "cm", "c.", "tsp.", "Tsp.", "tbsp.", "Tbsp.", "mililitres", "kg", "kilograms", "tsp", "tbsp"]


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
        self.description = None
        self.ingredients = []
        self.steps = []
        self.metas = []
        self.media_contents = []

    def reprJSON(self):
        return dict(title=self.title, alternate_title=self.alternate_title, description=self.description, ingredients=self.ingredients, steps=self.steps, metas=self.metas, media_contents=self.media_contents)

    class Description:
        def __init__(self, one_liner, paragraphs):
            self.one_liner = one_liner
            self.paragraphs = paragraphs

        def reprJSON(self):
            return dict(one_liner=self.one_liner, paragraphs=self.paragraphs)

    class Ingredient:
        def __init__(self, ingredient_id, name, quantity: float, unit: Unit, prep_hint: str):
            self.id = ingredient_id
            self.name = name
            self.quantity = quantity
            self.quantity_unit = unit
            self.prep_hint = prep_hint

        def reprJSON(self):
            return dict(id=self.id, name=self.name, quantity=self.quantity, quantity_unit=self.quantity_unit, prep_hint=self.prep_hint)

    class Step:
        def __init__(self, instruction, phase, time: timedelta, triggers, ingredients, resources):
            self.media_contents = []
            self.instruction = instruction
            self.phase = phase
            self.time = time
            self.triggers = triggers
            self.ingredients = ingredients
            self.resources = resources

        def reprJSON(self):
            return dict(media_contents=self.media_contents, instruction=self.instruction, phase=self.phase, time=self.time, triggers=self.triggers, ingredients=self.ingredients, resources=self.resources)

    class Meta:
        def __init__(self, cuisine: str, time_to_cook: timedelta, time_to_prep: timedelta, nutritional_values: _type.List[NutritionType], nutritional_tags, ratings: float, meal_type: MealType, regional_info):
            self.cuisine = cuisine
            self.time_to_cook = time_to_cook
            self.time_to_prep = time_to_prep
            self.nutritional_values = nutritional_values
            self.nutritional_tags = nutritional_tags
            self.ratings = ratings
            self.meal_type = meal_type
            self.regional_info = regional_info

        def reprJSON(self):
            return dict(cuisine=self.cuisine, time_to_cook=self.time_to_cook, time_to_prep=self.time_to_prep, nutritional_values=self.nutritional_values, ratings=self.ratings, meal_type=self.meal_type, regional_info=self.regional_info)

    class MediaContent:
        def __init__(self, resource_title: str, url: str):
            self.resource_title = resource_title
            self.url = url

        def reprJSON(self):
            return dict(resource_title=self.resource_title, url=self.url)


def get_quantity_identifier_regexp(quantity_identifiers):
    re_quantity_identifier_str = '\w*[' + \
        ''.join(quantity_identifiers) + ']\w*'
    quantity_identifier_regexp = '('+re_quantity_identifier_str+')'
    return quantity_identifier_regexp


def get_quantity_unit_identifier_regexp(quantity_unit_identifiers):
    re_quantity_unit_identifier_str = '(' + \
        '|'.join(quantity_unit_identifiers) + ')'
    quantity_unit_identifier_regexp = re_quantity_unit_identifier_str
    return quantity_unit_identifier_regexp


def parameterize_ingredient_phrase(phrase):
    quantity_identifier_regexp = get_quantity_identifier_regexp(
        quantity_identifiers)
    quantity_unit_identifier_regexp = get_quantity_unit_identifier_regexp(
        quantity_unit_identifiers)
    name = []
    name_string = ""
    quantity = []
    quantity_unit = []
    ingredient = []
    prep_hint = ""
    phrase = " ".join(re.split('(\d+)',phrase))
    doc = nlp(phrase)
    # print("-"*50)
    # print(phrase)
    deleted_tokens = []
    indices = {c.strip().replace(",", ""): i for i,
               c in enumerate(phrase.split())}
    # print(indices)
    for token in doc:
        # print(token.text," ",token.pos_," ",token.dep_," ",token.tag_," ",token.is_stop)
        if((token.pos_ in quantity_pos) or (token.tag_ in quantity_tag) or (re.fullmatch(quantity_identifier_regexp, token.lemma_))):
            quantity.append(token.text)
            deleted_tokens.append(token.i)
        elif(re.fullmatch(quantity_unit_identifier_regexp, token.lemma_)):
            quantity_unit.append(token.text)
            deleted_tokens.append(token.i)
        elif (((token.tag_ in ['NN']) or (token.dep_ in ['nsubj', 'ROOT'])) and (token.pos_ in ['NOUN', 'PROPN'])):
            name.append(token.text)
            for child in token.children:
                # print(child.text," ",child.pos_," ",child.dep_)
                if((child.dep_ in ['amod', 'compound'])):
                    name.append(child.text)
                    deleted_tokens.append(child.i)
            # name.append(token.text)
            # print(name)
            name = [*set(name)]
            # print("name set: ",name)
            deleted_tokens.append(token.i)
    try:
        name_string = " ".join(sorted(name, key=indices.get))
    except:
        # print("indices exception")
        name_string = " ".join(name)
    for k in quantity_unit + quantity:
        # print k
        name_string = name_string.replace(k, "").strip()
    remaining_phrase = []
    for token in doc:
        if token.i not in deleted_tokens:
            remaining_phrase.append(token.text + " ")
    doc = nlp("".join(remaining_phrase))
    prep_hint = "".join(remaining_phrase)
    # print("Remaining Phrase: {}".format("".join(remaining_phrase)))
    return [name_string, " ".join(quantity),
          " ".join(quantity_unit), prep_hint.strip()]


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
