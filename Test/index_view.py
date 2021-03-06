import re
import json
from django.shortcuts import render
from .getData import getData

def index(request):
    ctx = {}

    # 进行查询
    if(request.GET):
        context = {}
        query = request.GET['user_text'].rstrip(",")
        diseases = re.split("[,，]", query)
        for disease in diseases:
            # print(disease)
            links, nodes = getData(disease)
            if not nodes:
                ctx= {'title': '<h1>数据库中暂未添加该实体或者查询式输入错误！</h1>'}
                return render(request,"index.html",{'query': query, 'ctx':ctx})
            context[disease] = {"nodes": nodes, "links": links}
        return render(request, 'index.html', {'query': query, 'context': context})
            
    return render(request,"index.html", {'ctx':ctx})
