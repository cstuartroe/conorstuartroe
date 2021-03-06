from django.urls import path, re_path

from . import views

urlpatterns = [
    path('news', views.news, name='news'),
    path('wp', views.wp, name='wp'),
    path('projects', views.projects, name='projects'),
    path('guide/webtech', views.webguide, name='webguide'),
    path('clock', views.clock, name='clock'),
    path('calendar', views.calendar, name='calendar'),
    path('new_calendar', views.new_calendar, name='new_calendar'),
    path('negaternary', views.negaternary, name='negaternary'),
    path('negabinary', views.negabinary, name='negabinary'),
    path('amcyezs', views.amcyezs, name='amcyezs'),
    path('boxes', views.boxes, name='boxes'),
    path('boxdata', views.boxdata, name='boxdata'),
    path('boxreset', views.boxreset, name='boxreset'),
    path('randwords', views.randwords, name='randwords'),
    path('ajax', views.ajax, name='ajax'),
    path('ajaxblock', views.ajaxblock, name='ajaxblock'),
    path('tekotypes', views.tekotypes, name="tekotypes"),
    path('journal', views.journalhome, name="journalhome"),
    path('journal/<str:date_string>', views.journalentry, name="journalentry"),
    path('journal/md/<str:date_string>', views.journalmd, name="journalmd"),
    path('situations', views.situations, name="situations"),
    path('', views.index, name='index'),
    re_path(r'^.*/$', views.react_index, name="react_index")
]
