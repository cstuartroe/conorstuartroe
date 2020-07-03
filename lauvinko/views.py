from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import django.template
from lauvinko.lang.utils import LauvinkoError
from lauvinko.lang.dict import TheDictionary, Gloss

import json


def index(request):
    return render(request, 'react_index.html', {"app": "lauvinko", "title": "Lauvìnko"})


def page(request, name):
    try:
        return render(request, 'lauvinko/' + name + '.html')
    except django.template.exceptions.TemplateDoesNotExist:
        return HttpResponseRedirect('/lauvinko')


def gloss_api(request):
    outline = request.GET.get("outline", None).replace("_", " ").replace("~", "=")
    language = request.GET.get("lang")

    try:
        gloss = Gloss(outline, language)
        output = {"status": "success", "gloss": gloss.to_json()}
    except LauvinkoError as e:
        output = {"status": "failed", "reason": str(e)}
    return HttpResponse(json.dumps(output, indent=2), content_type='application/json')


def word_api(request):
    lemma_id = request.GET.get("id")
    
    try:
        output = {"status": "success", "entry": TheDictionary.lookup_lemma(lemma_id).to_json()}
    except LauvinkoError as e:
        output = {"status": "failed", "reason": str(e)}

    return HttpResponse(json.dumps(output, indent=2), content_type='application/json')


def dict_api(request):
    d = TheDictionary.to_json()
    output = {"status": "success", "length": len(d), "entries": d}
    
    return HttpResponse(json.dumps(output, indent=4), content_type='application/json')
