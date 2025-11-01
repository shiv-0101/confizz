from django.urls import path

from . import views

app_name = "confessions"

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
    path('confession/<int:pk>/summarize/', views.summarize_comments, name='summarize_comments'),
]
