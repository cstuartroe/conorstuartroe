from django.http import HttpResponseRedirect
from django.shortcuts import render
import django.template

def index(request):
    return render(request, 'lauvinko_index.html')

def page(request,name):
    try:
        return render(request, 'lauvinko/' + name + '.html')
    except django.template.exceptions.TemplateDoesNotExist:
        return HttpResponseRedirect('/lauvinko')
