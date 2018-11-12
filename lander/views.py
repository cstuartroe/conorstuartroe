from django.shortcuts import render
from django.http import HttpResponse
from .wpfetch import *
from .RSS_reader import *

def index(request):
    return render(request, 'lander/index.html')

def personal(request):
    return render(request, 'lander/personal.html')

def news(request):
    context = {'feed':get_feed()}
    return render(request, 'lander/news.html', context)

def wp(request):
    context = {'posts':get_worthwhile_posts()}
    return render(request, 'lander/wp.html', context)

def projects(request):
    return render(request, 'lander/projects.html')

def webguide(request):
    return render(request, 'lander/webguide.html')

def clock(request):
    return render(request, 'lander/clock.html')

def calendar(request):
    return render(request, 'lander/calendar.html')

def negaternary(request):
    return render(request, 'lander/negaternary.html')
