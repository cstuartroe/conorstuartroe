from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import django.template


def index(request):
    return render(request, 'games/index.html')
