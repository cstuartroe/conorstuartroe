from django.urls import path, re_path

from . import views

urlpatterns = [
    path('users', views.users, name="users"),
    path('games', views.games, name="games"),
    path('', views.index, name='index')
]
