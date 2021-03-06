from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import giphy_client
from giphy_client.rest import ApiException

from conorstuartroe.settings_secret import GIPHY_SEARCH_API

from random import randrange

from .models import User, GameInstance, Score, FeelinLuckySubmission, FeelinLuckyGuess


def index(request):
    return render(request, 'react_index.html', {"app": "games"})


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
        user = User.objects.get(username=request.POST.get("username"))
        gameInstance = GameInstance.objects.get(gameInstanceId=request.POST.get("gameInstance"))

        api_instance = giphy_client.DefaultApi()
        query = request.POST.get("query", "")
        response = api_instance.gifs_search_get(GIPHY_SEARCH_API, query, limit=10, rating='g',
                                                    lang='en', fmt='json')

        gif_url_list = [gif.images.downsized.url for gif in response.data]

        if len(gif_url_list) > 2:
            sub = FeelinLuckySubmission(author=user, gameInstance=gameInstance, search_query=request.POST.get("query", ""),
                                    candidates=','.join(gif_url_list))
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

        # gameInstance.accepting_joins = False
        # gameInstance.save()

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


def add_score(user, gameInstance, points):
    try:
        score = Score.objects.get(player=user, gameInstance=gameInstance)
    except Score.DoesNotExist:
        score = Score(player=user, gameInstance=gameInstance, value=0)

    score.value += points
    score.save()


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

        if (guesser != submission.author) and (author == submission.author):
            add_score(submission.author, submission.gameInstance, -1)

        guesses = FeelinLuckyGuess.objects.filter(submission=submission)
        participants = submission.gameInstance.participants.all()

        if len(guesses) == len(participants):
            correct_query_guesses = 0
            for g in guesses:
                if g.search_query == submission.search_query and g.guesser != submission.author:
                    correct_query_guesses += 1

            if correct_query_guesses >= (len(participants)/2):
                for user in participants:
                    if user != submission.author:
                        add_score(user, submission.gameInstance, 1)
            else:
                add_score(submission.author, submission.gameInstance, len(participants) - 1)

        return HttpResponse()


@csrf_exempt
def scores(request):
    if request.method == "GET":
        gameInstance = request.GET.get("gameInstance")
        scores = [model_to_dict(s) for s in Score.objects.filter(gameInstance=gameInstance)]
        return JsonResponse(scores, safe=False)
