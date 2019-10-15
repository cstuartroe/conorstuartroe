from django.urls import path, re_path

from . import views

urlpatterns = [
    path('users', views.users, name="users"),
    path('games', views.games, name="games"),
    path('new_game', views.new_game, name="new_game"),
    path('join_game', views.join_game, name="join_game"),
    path('feelin_lucky/search', views.feelin_lucky_search, name="feelin_lucky_search"),
    path('feelin_lucky/select', views.feelin_lucky_select, name="feelin_lucky_select"),
    path('feelin_lucky/submissions', views.feelin_lucky_submissions, name="feelin_lucky_submissions"),
    path('feelin_lucky/guess', views.feelin_lucky_guess, name="feelin_lucky_guess"),
    path('', views.index, name='index')
]
