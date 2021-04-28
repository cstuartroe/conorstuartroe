from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .wpfetch import *
from .RSS_reader import *
from .randwords import *
import json
import datetime
import os


def react_index(request):
    return render(request, 'react_index.html')


def index(request):
    return render(request, 'index.html')


def news(request):
    context = {'feed': get_feed()}
    return render(request, 'news.html', context)


def wp(request):
    context = {'posts': get_worthwhile_posts()}
    return render(request, 'wp.html', context)


def projects(request):
    return render(request, 'projects.html')


def webguide(request):
    return render(request, 'webguide.html')


def clock(request):
    return render(request, 'clock.html')


def calendar(request):
    return render(request, 'calendar.html')


def new_calendar(request):
    return render(request, 'calendar2.html')


def negaternary(request):
    return render(request, 'negaternary.html')


def negabinary(request):
    return render(request, 'negabinary.html')


def amcyezs(request):
    return render(request, 'amcyezs.html')


def boxes(request):
    return render(request, 'boxes.html')


def boxdata(request):
    x = request.GET["x"]
    y = request.GET["y"]
    user = request.GET["user"]
    with open("boxdata.json","r") as fh:
        data = json.load(fh)
    data[user] = {"x":x, "y":y}
    with open("boxdata.json","w") as fh:
        json.dump(data,fh,indent=4)
    return HttpResponse(json.dumps(data,indent=4),content_type='application/json')


def boxreset(request):
    with open('boxdata.json','w') as fh:
        fh.write("{}")
    return HttpResponseRedirect('/boxes')


def randwords(request):
    clearseed()
    pattern = request.GET.get("q",randpattern())
    words = genwords(pattern)
    return render(request, 'randwords.html', {"words": words})


def ajax(request):
    return render(request, 'ajax.html')


def ajaxblock(request):
    return HttpResponse("If you want to understand recursion, you'll have to ask someone smarter than me, who will tell you \"")


def tekotypes(request):
    return render(request, 'teko-types.html')


def shifted_today(offset=-5):
    return (datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=offset)))).date()


def journalhome(request):
    dates = [(shifted_today().strftime("%Y%m%d"), "ejesoM")]

    for filename in os.listdir("static/md"):
        try:
            d = datetime.datetime.strptime(filename, "%Y%m%d.md")
            if d.date() != shifted_today():
                link = filename[:8]
                title = f"{filename[:4]}.{filename[4:6]}.{filename[6:8]}"
                dates.append((link, title))

        except ValueError:
            pass

    dates.sort(key=lambda x: x[0], reverse=True)

    return render(request, 'journal-home.html', {"dates": dates})


def journalentry(request, date_string):
    try:
        d = datetime.datetime.strptime(date_string, "%Y%m%d")
    except ValueError:
        return HttpResponse("Please use a valid date")

    context = {
        "year": date_string[:4],
        "month": date_string[4:6],
        "day": date_string[6:],
        "today": d.date() == shifted_today()
    }
    return render(request, 'journal-entry.html', context)


def journalmd(request, date_string):
    try:
        datetime.datetime.strptime(date_string, "%Y%m%d")
    except ValueError:
        return HttpResponse("Please use a valid date")

    filename = f"static/md/{date_string}.md"

    if request.method == "GET":
        try:
            with open(filename, "r") as fh:
                md = fh.read()
        except FileNotFoundError:
            md = ""

        return HttpResponse(md)

    elif request.method == "POST":
        with open(filename, "w") as fh:
            fh.write(request.POST["md"])
        return HttpResponse()


def situations(request):
    return render(request, "situations.html")