from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<str:user_name>/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
    
]