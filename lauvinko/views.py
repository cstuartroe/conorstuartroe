from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import django.template
from lauvinko.lang.utils import *

import json

def index(request):
    return render(request, 'lauvinko_index.html')

def page(request,name):
    try:
        return render(request, 'lauvinko/' + name + '.html')
    except django.template.exceptions.TemplateDoesNotExist:
        return HttpResponseRedirect('/lauvinko')

def gloss_api(request):
    outline = request.GET.get("outline",None).replace("_"," ")
    language = request.GET.get("language","lv")

    dictionary = KasanicDictionary()
    try:
        gloss = Gloss(outline,dictionary,language)
        output = {"status":"success","gloss":gloss.fields,"length":gloss.length}
    except LauvinkoError as e:
        output = {"status":"failed","reason":str(e)}
    return HttpResponse(json.dumps(output,indent=4),content_type='application/json')

def dict_api(request):
    stem_id = request.GET.get("stem_id")
    dictionary = KasanicDictionary()
    
    try:
        output = {"status":"success","entry":dictionary.lookup_stem(stem_id).to_json()}
    except LauvinkoError as e:
        output = {"status":"failed","reason":str(e)}
    return HttpResponse(json.dumps(output,indent=4),content_type='application/json')

def wholedict_api(request):
    stem_id = request.GET.get("stem_id")
    dictionary = KasanicDictionary()
        
    output = {"status":"success","length":len(dictionary.entries),"entries":{}}
    for ident,entry in dictionary.entries.items():
        output["entries"][ident] = entry.to_json()
    
    return HttpResponse(json.dumps(output,indent=4),content_type='application/json')
