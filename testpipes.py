import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_ingredients(ingredient_string):
  ingredients = []

  # Split the ingredient string into individual ingredients
  split_ingredients = re.split(",(?=\s[^&])", ingredient_string)

  for ingredient in split_ingredients:
    # Parse the ingredient string with spaCy
    doc = nlp(ingredient)

    # Extract the ingredient name
    ingredient_name = [token.text for token in doc if token.pos_ == "NOUN"]
    ingredient_name = " ".join(ingredient_name)

    # Extract the ingredient quantity and unit of measurement
    quantity = None
    unit = None
    for token in doc:
      if token.pos_ == "NUM":
        quantity = token.text
      elif token.pos_ == "NOUN" and token.text.lower() in ["tsp", "tbsp", "cup", "pint", "quart", "gallon", "ounce", "pound"]:
        unit = token.text
      elif token.pos_ == "ADJ" and token.text.lower() in ["large", "small", "medium"]:
        unit = token.text
      
    # Extract any additional comments
    comments = []
    for token in doc:
      if token.text.lower() == "and":
        break
      elif token.pos_ == "ADV":
        comments.append(token.text)
    comments = " ".join(comments)
      
    # Add the ingredient information to the list of ingredients
    ingredients.append({
      "name": ingredient_name,
      "quantity": quantity,
      "unit": unit,
      "comments": comments
    })
    
  return ingredients

ingredient_string = "1 large potato, cooked until just soft & grated, 4 curry leaves, chopped, handful of fresh coriander leaves, mustard oil for frying, 1 tsp turmeric, 5¾ fresh chilli, finely chopped, ½ tsp Kashmiri chilli powder, ½ tsp Kashmiri chilli powder, 1/2 tsp nothing"

ingredients = extract_ingredients(ingredient_string)

print(ingredients)
