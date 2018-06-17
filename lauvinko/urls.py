from django.urls import path, re_path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    re_path(r'(?P<name>[a-z]+)',views.page)
]
