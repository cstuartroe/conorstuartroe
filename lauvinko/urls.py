from django.urls import path, re_path

from . import views

urlpatterns = [
    path('gloss', views.gloss_api),
    path('dict', views.dict_api),
    path('word', views.word_api),
    re_path(r'.*$', views.index),
]
