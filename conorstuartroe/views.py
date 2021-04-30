from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime
import os

from .randwords import clearseed, randpattern, genwords
from .twitter import api, tweet_to_json


def react_index(request):
    return render(request, 'react_index.html')


def index(request):
    return render(request, 'index.html')


def projects(request):
    return render(request, 'projects.html')


def clock(request):
    return render(request, 'clock.html')


def calendar(request):
    return render(request, 'calendar.html')


def negaternary(request):
    return render(request, 'negaternary.html')


def negabinary(request):
    return render(request, 'negabinary.html')


def randwords(request):
    clearseed()
    pattern = request.GET.get("q",randpattern())
    words = genwords(pattern)
    return render(request, 'randwords.html', {"words": words})


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


HACK_HOUSE_ACCOUNTS = [
    'cstuartroe',
    'dkb868',
    'vvhuang_',
    'vroomerify',
    'kayolord',
    'apagajewski',
]


def tweetlist(request):
    tweets = []
    for username in HACK_HOUSE_ACCOUNTS:
        for status in api.user_timeline(screen_name=username):
            tweets.append(tweet_to_json(status))

    tweets.sort(key=lambda t: t["created_at"], reverse=True)

    return JsonResponse(tweets[:20], safe=False)
