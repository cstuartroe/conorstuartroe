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
