"""
URL configuration for confizz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# confizz/urls.py
from django.contrib import admin
from django.urls import path, include
from confessions import views as confessions_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # include home app urls for the root path
    path("", include("home.urls")),
    # include confessions app urls with a prefix
    path("confessions/", include("confessions.urls", namespace="confessions")),
    # direct path to fizzzones
    path("fizzzones/", confessions_views.fizzzones, name="fizzzones"),
]
    

   