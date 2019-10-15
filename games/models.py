from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10, unique=True, primary_key=True)
    screen_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.username


class Game(models.Model):
    slug = models.CharField(max_length=20, unique=True, primary_key=True)
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.slug


class GameInstance(models.Model):
    gameInstanceId = models.CharField(max_length=4, unique=True, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default='situations')
    participants = models.ManyToManyField(User)
    accepting_joins = models.BooleanField(default=True)


class Score(models.Model):
    player = models.ForeignKey(Game, on_delete=models.CASCADE, default='situations')
    gameInstance = models.ForeignKey(GameInstance, on_delete=models.CASCADE, default='')
    value = models.IntegerField(default=0)


class FeelinLuckySubmission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    gameInstance = models.ForeignKey(GameInstance, on_delete=models.CASCADE, default='')
    search_query = models.CharField(max_length=30)
    filename = models.CharField(max_length=50)


class FeelinLuckyGuess(models.Model):
    guesser = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    submission = models.ForeignKey(FeelinLuckySubmission, on_delete=models.CASCADE, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name="authorship_guess")
    search_query = models.CharField(max_length=30)