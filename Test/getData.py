import json
import os

def getData(disease):
    nodes = None
    links = None
    file = disease.lower() + ".json"
    files = os.listdir("pathways/")
    if file in files:
        with open("pathways/" + file, encoding="utf-8") as f:
            data = json.load(f)
            nodes = data["nodes"]
            links = data["links"]
    return links, nodes