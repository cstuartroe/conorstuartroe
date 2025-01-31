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
    path('clock', views.clock, name='clock'),
    path('negaternary', views.negaternary, name='negaternary'),
    path('negabinary', views.negabinary, name='negabinary'),
    path('randwords', views.randwords, name='randwords'),
    path('journal', views.journalhome, name="journalhome"),
    path('journal/<str:date_string>', views.journalentry, name="journalentry"),
    path('journal/md/<str:date_string>', views.journalmd, name="journalmd"),
    re_path(r'^.*$', views.react_index, name="react_index")
]
