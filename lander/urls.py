from django.urls import path

from . import views

urlpatterns = [
    path('personal', views.personal, name='personal'),
    path('news', views.news, name='news'),
    path('wp', views.wp, name='wp'),
    path('projects', views.projects, name='projects'),
    path('guide/webtech', views.webguide, name='webguide'),
    path('clock', views.clock, name='clock'),
    path('calendar', views.calendar, name='calendar'),
    path('', views.index, name='index')
]
