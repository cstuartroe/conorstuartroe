"""conorstuartroe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
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
