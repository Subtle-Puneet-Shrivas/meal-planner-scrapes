import spacy
from common_files.recipe_handler import Recipe, parameterize_ingredient_phrase, ComplexEncoder
from common_files.mogodb_functions import postRecipe
from common_files.s3_functions import upload_image_to_s3
import re
from PIL import Image
from io import StringIO
from datetime import datetime, timedelta
import csv
import json
import time
import os
from json_tricks import dump, dumps, load, loads, strip_comments

def load_csv(filename):
    rows = []
    f = open(filename)
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)
    f.close()
    return rows

data = load_csv("C:\Users\punee\Downloads\archive\cuisines.csv")
print(data[0])

