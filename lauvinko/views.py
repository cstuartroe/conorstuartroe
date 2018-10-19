from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import django.template
from .utils import *

import json

def index(request):
    return render(request, 'lauvinko_index.html')

def page(request,name):
    try:
        return render(request, 'lauvinko/' + name + '.html')
    except django.template.exceptions.TemplateDoesNotExist:
        return HttpResponseRedirect('/lauvinko')

def gloss_api(request):
    try:
        outline = request.GET.get("outline",None).replace("_"," ")
        language = request.GET.get("language","lv")

        dictionary = KasanicDictionary()
        gloss = Gloss(outline,dictionary,language)
        
        output = {"status":"success","gloss":gloss.fields,"length":gloss.length}
    except BaseException as e:
        output = {"status":"fail","message":str(e)}
    return HttpResponse(json.dumps(output,indent=4),content_type='application/json')

def dict_api(request):
##    try:
    stem_id = request.GET.get("stem_id")
    dictionary = KasanicDictionary()
    
    output = {"status":"success","entry":dictionary.entries[stem_id].to_json()}
##    except BaseException as e:
##        output = {"status":"fail","message":str(e)}
    return HttpResponse(json.dumps(output,indent=4),content_type='application/json')

def wholedict_api(request):
    try:
        stem_id = request.GET.get("stem_id")
        dictionary = KasanicDictionary()
        
        output = {"status":"success","length":len(dictionary.entries),"entries":{}}
        for ident,entry in dictionary.entries.items():
            output["entries"][ident] = entry.to_json()
    except BaseException as e:
        output = {"status":"fail","message":str(e)}
    return HttpResponse(json.dumps(output,indent=4),content_type='application/json')
