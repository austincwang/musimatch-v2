from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('join/', views.join_game, name='join'),
]