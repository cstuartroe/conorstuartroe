from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from google_images_search import GoogleImagesSearch
from conorstuartroe.settings_secret import GOOGLE_SEARCH_API, SEARCH_ENGINE_ID

from random import randrange

from .models import User, Game, GameInstance


def index(request):
    return render(request, 'games/index.html')


def users(request):
    if request.method == "GET":
        userlist = [model_to_dict(u) for u in User.objects.all()]
        return JsonResponse(userlist, safe=False)


def games(request):
    if request.method == "GET":
        gamelist = [model_to_dict(u) for u in Game.objects.all()]
        return JsonResponse(gamelist, safe=False)


@csrf_exempt
def new_game(request):
    if request.method == "POST":
        gameInstanceId = ""
        for i in range(4):
            gameInstanceId += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[randrange(26)]

        game = Game.objects.get(slug=request.POST.get("game"))
        gi = GameInstance(gameInstanceId=gameInstanceId, game=game)
        gi.save()

        first_participant = User.objects.get(username=request.POST.get("username"))
        gi.participants.add(first_participant)
        gi.save()

        return JsonResponse({"gameInstance": gameInstanceId})


@csrf_exempt
def join_game(request):
    if request.method == "POST":
        try:
            gameInstance = GameInstance.objects.get(gameInstanceId=request.POST.get("gameInstance").upper())
        except GameInstance.DoesNotExist:
            return JsonResponse({"accepted": False})

        user = User.objects.get(username=request.POST.get("username"))
        if user not in gameInstance.participants.all():
            gameInstance.participants.add(user)
            gameInstance.save()

        return JsonResponse({"accepted": True})


@csrf_exempt
def feelin_lucky_search(request):
    if request.method == "POST":
        gis = GoogleImagesSearch(GOOGLE_SEARCH_API, SEARCH_ENGINE_ID)
        gis.search(search_params={
            'q': request.POST.get("query", ""),
            'num': 4,
            'safe': 'off'
        })

        imagelist = []
        for image in gis.results():
            image.download('games/static/img/feelin_lucky_downloads/')
            filename = image.path.split("/")[-1]
            imagelist.append(filename)

        return JsonResponse(imagelist, safe=False)


@csrf_exempt
def feelin_lucky_select(request):
    if request.method == "POST":
        return HttpResponse()
