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
    # community urls at root level
    path("communities/", confessions_views.community_list, name="community-list"),
    path("communities/create/", confessions_views.community_create, name="community-create"),
    path("communities/<slug:slug>/", confessions_views.community_detail, name="community-detail"),
    path("communities/<slug:slug>/delete/", confessions_views.community_delete, name="community-delete"),
]
    

   