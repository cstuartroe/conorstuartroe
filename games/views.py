from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse

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
