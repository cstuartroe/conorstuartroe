from django.shortcuts import render
from .pagenames import *

def index(request):
    return render(request, 'lauvinko/index.html')

def page(request,name):
    ID = pagenames[name]
    return render(request, 'lauvinko/' + ID + '.html')
