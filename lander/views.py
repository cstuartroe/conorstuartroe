from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .wpfetch import *
from .RSS_reader import *
from .randwords import *
import json

def index(request):
    return render(request, 'lander/index.html')

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

def new_calendar(request):
    return render(request, 'lander/calendar2.html')

def negaternary(request):
    return render(request, 'lander/negaternary.html')

def negabinary(request):
    return render(request, 'lander/negabinary.html')

def amcyezs(request):
    return render(request, 'lander/amcyezs.html')

def boxes(request):
    return render(request, 'lander/boxes.html')

def boxdata(request):
    x = request.GET["x"]
    y = request.GET["y"]
    user = request.GET["user"]
    with open("lander/boxdata.json","r") as fh:
        data = json.load(fh)
    data[user] = {"x":x, "y":y}
    with open("lander/boxdata.json","w") as fh:
        json.dump(data,fh,indent=4)
    return HttpResponse(json.dumps(data,indent=4),content_type='application/json')

def boxreset(request):
    with open('lander/boxdata.json','w') as fh:
        fh.write("{}")
    return HttpResponseRedirect('/boxes')

def randwords(request):
    clearseed()
    pattern = request.GET.get("q",randpattern())
    words = genwords(pattern)
    return render(request, 'lander/randwords.html', {"words":words})

def ajax(request):
    return render(request, 'lander/ajax.html')

def ajaxblock(request):
    return HttpResponse("If you want to understand recursion, you'll have to ask someone smarter than me, who will tell you \"")
