from django.urls import path, re_path

from . import views

urlpatterns = [
    path('users', views.users, name="users"),
    path('games', views.games, name="games"),
    path('new_game', views.new_game, name="new_game"),
    path('join_game', views.join_game, name="join_game"),
    path('feelin_lucky_search', views.feelin_lucky_search, name="feelin_lucky_search"),
    path('feelin_lucky_select', views.feelin_lucky_select, name="feelin_lucky_select"),
    path('', views.index, name='index')
]
