from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'(?P<name>[a-z0-9_]+)',views.page),
    path('', views.index, name='index')
]
