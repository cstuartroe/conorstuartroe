from django.urls import path, re_path

from . import views

urlpatterns = [
    path('gloss',views.gloss_api),
    path('dict',views.dict_api),
    path('dictall',views.wholedict_api),
    re_path(r'(?P<name>[a-z0-9_]+)',views.page),
    path('', views.index, name='index')
]
