from django.http import HttpResponse
import json
import re
from collections import defaultdict

def getReaction(request):
    treatments = []
    reactions = defaultdict(dict)
    snodes = request.GET['snodes'].strip().split("\t")
    #print(len(snodes))
    for snode in snodes:
        items = snode.rstrip(";").split("/")
        treatment = items[0]
        drugs = items[1].split(";")
        for drug in drugs:
            drug_name, elem = drug.split(",")
            treatments.append((treatment + "(" + drug_name + ")", elem))
    
    with open("reaction.json", encoding="utf-8") as f:
        savedReactions = json.load(f)

    for i in range(len(treatments)-1):
        for j in range(i+1, len(treatments)):
            if treatments[i][1] + "," + treatments[j][1] in savedReactions:
                key = treatments[i][0] + "," + treatments[j][0]
                elem = treatments[i][1] + "," + treatments[j][1]
                props = savedReactions[elem].split("|")
                reactions[key]["elem"] = elem
                reactions[key]["significance"] = props[0]
                reactions[key]["reaction mechanism"] = props[1]
                reactions[key]["url"] = props[2]
                reactions[key]["to_consumer"] = props[3]
                reactions[key]["to_professor"] = props[4]
    
    data = {"reactions": reactions}
    if reactions:
        data["flag"] = True
    else:
        data["flag"] = False
    # print(reactions)
    return HttpResponse(json.dumps(data), content_type='application/json')