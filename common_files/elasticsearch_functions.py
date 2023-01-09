from elasticsearch import Elasticsearch
import json
import datetime
# es = Elasticsearch(
#     cloud_id="recipe_bhandaar:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ2NTk2MzNlMDM4Mzc0YTcxYTMxYjBlM2VjOGUwMzIyNSRiZmEzNzdkNTY0NDM0YzUyYWE3OGEyMzIzMGViOWI4Ng==",
#     bearer_auth=('puneet-shrivas', 'KmAs1t0dQf6bvMNv7QqMzg'),
# )
es = Elasticsearch(
    "https://recipe-bhandaar.es.us-central1.gcp.cloud.es.io:9243/",
    basic_auth=('elastic', 'mTOFdE47BJOcrdCHZ7RKXv5l'),
)

# es = Elasticsearch(["https://recipe-bhandaar.es.us-central1.gcp.cloud.es.io"],
#                    http_auth=("recipe-chef","VGTkFWg1S-WLGkOsqUw1dQ"),
#                    scheme="https",
#                    port=443
#                    )
print(es.info)
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.'
}
res = es.index(index="search-recipes", id=1, document=doc)
print(res['result'])

def postRecipeElastic(recipe_object,id):
    resp = es.index(index='search-recipes',id=id, document=recipe_object)
    return resp


res = es.get(index="search-recipes", id=1)
print(res['_source'])
