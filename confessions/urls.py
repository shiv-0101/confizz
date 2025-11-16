from django.urls import path

from . import views

app_name = "confessions"

urlpatterns = [
    path("", views.confession_list, name="confession_list"),
    path('confession/<int:pk>/summarize/', views.summarize_comments, name='summarize_comments'),
    path('confession/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('add_anonymous_confession/', views.confession_list, name='add_anonymous_confession'),  # Reuse confession_list view
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("hello/", views.hello_world, name="hello_world"),
    path("fizzzones/", views.fizzzones, name="fizzzones"),
]
