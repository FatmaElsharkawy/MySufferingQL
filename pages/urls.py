from django.urls import path
from . import views

urlpatterns=[
path("", views.index, name="registeration-page"),
path("login", views.login, name="login-page"),
path('authenticate/', views.authenticate_user, name='authenticate_user'),
]
