# game/urls.py

from django.urls import path
from .views import home, register, game_view, leaderboard, feedback_view, contact_us, user_profile, login_view, logout_view,guess,result




urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('game/', game_view, name='game'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('feedback/', feedback_view, name='feedback'),
    path('contact/', contact_us, name='contact_us'),
    path('profile/', user_profile, name='profile'),
     path('guess/', guess, name='guess'),  # Guess page
    path('result/', result, name='result'),  # Result page
]
