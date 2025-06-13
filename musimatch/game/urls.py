from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('join/', views.join_game, name='join'),
    path('play_random_song/', views.play_random_song, name='play_random_song'), 
    path('artist/', views.artist_search, name='artist_search'),
    path('artist/taylor_swift', views.taylor_swift_guess, name='taylor_swift_guess'),
    path('genre_search/', views.genre_search, name='genre_search'),
    path('genre/', views.play_by_genre, name='play_by_genre'),
    path('time_period_search/', views.time_period_search, name='time_period_search'),
    path('time_period/', views.play_by_time_period, name='play_by_time_period'),
]