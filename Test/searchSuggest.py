from django.http import HttpResponse
 
import json
import re
 
def searchSuggest(request):
    q = request.GET['q'].lower()
    key = re.split("[,，]", q)
    suggest = []
    with open("diseases.csv", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith(key[-1]):
                if(len(key[: -1]) > 0):
                    suggest.append(",".join(key[: -1]) + "," + line)
                else:
                    suggest.append(line)
    
    return HttpResponse(json.dumps(suggest), content_type='application/json')
