from django.contrib import admin

from .models import User, Game, GameInstance, Score, FeelinLuckySubmission, FeelinLuckyGuess

admin.site.register(User)
admin.site.register(Game)
admin.site.register(GameInstance)
admin.site.register(Score)
admin.site.register(FeelinLuckySubmission)
admin.site.register(FeelinLuckyGuess)
