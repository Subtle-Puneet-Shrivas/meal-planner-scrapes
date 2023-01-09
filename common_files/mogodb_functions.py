import pymongo
client = pymongo.MongoClient("mongodb+srv://puneet-shrivas:dhaniya@recipe-cluster.jddl1o8.mongodb.net/?retryWrites=true&w=majority")
db = client.recipes_test

def postRecipe(recipe_object):
    recipes=db.recipes
    recipe_id = recipes.insert_one(recipe_object).inserted_id
    return recipe_id

def getclientdb():
    return db

