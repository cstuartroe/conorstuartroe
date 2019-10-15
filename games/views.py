from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from google_images_search import GoogleImagesSearch
from conorstuartroe.settings_secret import GOOGLE_SEARCH_API, SEARCH_ENGINE_ID

from random import randrange

from .models import User, GameInstance, Score, FeelinLuckySubmission, FeelinLuckyGuess


def index(request):
    return render(request, 'games/index.html')


def users(request):
    if request.method == "GET":
        userlist = [model_to_dict(u) for u in User.objects.all()]
        userlist.sort(key=lambda x: x["screen_name"])
        return JsonResponse(userlist, safe=False)


@csrf_exempt
def new_game(request):
    if request.method == "POST":
        gameInstanceId = ""
        for i in range(4):
            gameInstanceId += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[randrange(26)]

        game = request.POST.get("game")
        gi = GameInstance(gameInstanceId=gameInstanceId, game=game, accepting_joins=True)
        gi.save()

        first_participant = User.objects.get(username=request.POST.get("username"))
        gi.participants.add(first_participant)
        gi.save()

        return JsonResponse({"gameInstance": gameInstanceId})


@csrf_exempt
def join_game(request):
    if request.method == "POST":
        game = request.POST.get("game")
        try:
            gameInstance = GameInstance.objects.get(game=game, gameInstanceId=request.POST.get("gameInstance").upper())
        except GameInstance.DoesNotExist:
            return JsonResponse({"accepted": False, "message": "No such game room."})

        user = User.objects.get(username=request.POST.get("username"))
        if user not in gameInstance.participants.all():
            if not gameInstance.accepting_joins:
                return JsonResponse({"accepted": False, "message": "That room is no longer accepting new players."})

            gameInstance.participants.add(user)
            gameInstance.save()

        return JsonResponse({"accepted": True})


@csrf_exempt
def participants(request):
    if request.method == "GET":
        try:
            gameInstance = GameInstance.objects.get(gameInstanceId=request.GET.get("gameInstance").upper())
        except GameInstance.DoesNotExist:
            return JsonResponse({"accepted": False, "message": "No such game room."})

        usernames = [user.username for user in gameInstance.participants.all()]
        return JsonResponse({"accepted": True, "participants": usernames})


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

        user = User.objects.get(username=request.POST.get("username"))
        gameInstance = GameInstance.objects.get(gameInstanceId=request.POST.get("gameInstance"))
        sub = FeelinLuckySubmission(author=user, gameInstance=gameInstance, search_query=request.POST.get("query", ""),
                                    candidates=','.join(imagelist))
        sub.save()

        return HttpResponse()


@csrf_exempt
def feelin_lucky_select(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST.get("username"))
        gameInstance = GameInstance.objects.get(gameInstanceId=request.POST.get("gameInstance"))
        sub = FeelinLuckySubmission.objects.get(author=user, gameInstance=gameInstance)
        sub.filename = request.POST.get("selection")
        sub.save()

        gameInstance.accepting_joins = False
        gameInstance.save()

        return HttpResponse()


@csrf_exempt
def feelin_lucky_submissions(request):
    if request.method == "GET":
        gameInstance = GameInstance.objects.get(gameInstanceId=request.GET.get("gameInstance"))
        sublist = [model_to_dict(s) for s in FeelinLuckySubmission.objects.filter(gameInstance=gameInstance)]
        sublist.sort(key=lambda x: x["id"])

        all_submissions = (len(sublist) == len(gameInstance.participants.all())) and all(sub["filename"] != "" for sub in sublist)

        response = {
            "submissions": sublist,
            "all_submissions": all_submissions
        }

        return JsonResponse(response)


@csrf_exempt
def feelin_lucky_guess(request):
    if request.method == "GET":
        gameInstance = GameInstance.objects.get(gameInstanceId=request.GET.get("gameInstance"))
        guesslist = [model_to_dict(g) for g in FeelinLuckyGuess.objects.all()
                     if g.submission.gameInstance == gameInstance]

        return JsonResponse(guesslist, safe=False)

    elif request.method == "POST":
        guesser = User.objects.get(username=request.POST.get("guesser"))
        submission = FeelinLuckySubmission.objects.get(id=request.POST.get("submissionId"))
        author = User.objects.get(username=request.POST.get("author"))
        search_query = request.POST.get("searchQuery")

        guess = FeelinLuckyGuess(guesser=guesser, submission=submission, author=author, search_query=search_query)
        guess.save()

        return HttpResponse()