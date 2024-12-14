from django.shortcuts import render

# Create your views here.
# game/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Game, Feedback
import random

def home(request):
    return render(request, 'game/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('game')
    else:
        form = UserCreationForm()
    return render(request, 'game/register.html', {'form': form})

#-----------------
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Game  # Make sure to import your Game model

# Define difficulty ranges
DIFFICULTY_RANGES = {
    'easy': (0, 99),
    'medium': (0, 999),
    'hard': (0, 9999)
}

def game_view(request):
    if request.method == 'POST':
        difficulty = request.POST.get('difficulty')
        # Get the correct range based on selected difficulty
        min_value, max_value = DIFFICULTY_RANGES.get(difficulty, (0, 99))  # Default to 'easy' if no difficulty selected
        target_number = random.randint(min_value, max_value)

        # Create a new game entry
        game = Game.objects.create(
            user=request.user,
            attempts=0,  # Starting attempts
            score=0,  # Starting score
            level=difficulty,
            target_number=target_number  # Store the target number
        )

        request.session['target_number'] = target_number  # Store target number in session
        request.session['difficulty'] = difficulty
        request.session['attempts'] = 0  # Track the number of attempts
        request.session['game_id'] = game.id  # Store game ID to update it later

        return redirect('guess')

    return render(request, 'game/start_game.html')

def guess(request):
    target_number = request.session.get('target_number')
    difficulty = request.session.get('difficulty', 'easy')
    attempts = request.session.get('attempts', 0)

    # Retrieve the game instance using the stored game ID
    game_id = request.session.get('game_id')
    game_instance = Game.objects.get(id=game_id)  # Fetch the game instance

    if request.method == 'POST':
        user_guess = int(request.POST.get('guess'))
        attempts += 1
        request.session['attempts'] = attempts

        if user_guess == target_number:
            # Update game result on successful guess
            game_instance.attempts = attempts
            game_instance.score = 100 - (attempts * 10)  # Example score calculation
            game_instance.save()  # Save the updated game instance

            return render(request, 'game/result.html', {
                'result': 'correct',
                'attempts': attempts,
                'difficulty': difficulty,
            })
        elif user_guess > target_number:
            hint = "Too high!"
        else:
            hint = "Too low!"

        if attempts >= 10:  # Max attempts
            # Save game result on failed guess
            game_instance.attempts = attempts
            game_instance.score = 0  # No score on failure
            game_instance.save()  # Save the updated game instance
            
            return render(request, 'game/result.html', {
                'result': 'failed',
                'target_number': target_number,
                'difficulty': difficulty,
            })

        return render(request, 'game/guess.html', {
            'hint': hint,
            'attempts': attempts,
            'difficulty': difficulty
        })

    return render(request, 'game/guess.html', {
        'attempts': attempts,
        'difficulty': difficulty
    })


def result(request):
    target_number = request.session.get('target_number')
    attempts = request.session.get('attempts')
    game_id = request.session.get('game_id')
     
    result = 'success' if request.session.get('attempts') <= 10 else 'failure'
    
    return render(request, 'game/result.html', {
        'result': result,
        'target_number': target_number,
        'attempts': attempts
    })

#-------------------


from django.db.models import Max

from django.db.models import Max
from django.contrib.auth.decorators import login_required

@login_required  # Ensure only logged-in users can access the leaderboard
def leaderboard(request):
    # Get the top 10 players sorted by score in descending order
    top_players = Game.objects.values('user__username').annotate(max_score=Max('score')).order_by('-max_score')[:10]

    return render(request, 'game/leaderboard.html', {
        'top_players': top_players
    })


def feedback_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Feedback.objects.create(user=request.user, content=content)
            messages.success(request, "Feedback submitted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Feedback cannot be empty!")
    return render(request, 'game/feedback.html')

def contact_us(request):
    return render(request, 'game/contact_us.html')

from django.db.models import Max

from django.db.models import Max

def user_profile(request):
    # Get the current user's game data
    games = Game.objects.filter(user=request.user)
    total_games = games.count()
    total_wins = games.filter(score__gt=0).count()
    best_score = games.order_by('-score').first()
    best_score_value = best_score.score if best_score else 0

    # Fetch leaderboard data: top scores from all users
    leaderboard = (
        Game.objects.values('user__username')
        .annotate(highest_score=Max('score'))
        .order_by('-highest_score')[:10]  # Get top 10 users
    )

    leaderboard_data = [
        {
            'username': entry['user__username'],
            'highest_score': entry['highest_score']
        }
        for entry in leaderboard
    ]

    return render(request, 'game/profile.html', {
        'games': games,
        'total_games': total_games,
        'total_wins': total_wins,
        'best_score': best_score_value,
        'leaderboard': leaderboard_data  # Pass leaderboard data as serializable
    })





# game/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
        else:
            return render(request, 'game/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'game/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')

# game/views.py

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # Get the current user's game data
    games = Game.objects.filter(user=request.user)
    total_games = games.count()
    total_wins = games.filter(score__gt=0).count()
    best_score = games.order_by('-score').first()
    best_score_value = best_score.score if best_score else 0

    # Pass the games to the template
    return render(request, 'game/profile.html', {
        'games': games,
        'total_games': total_games,
        'total_wins': total_wins,
        'best_score': best_score_value,
    })

