

# Create your models here.
# game/models.py

from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    target_number = models.IntegerField(default=0)  # Store the target number for reference

    def __str__(self):
        return f"{self.user.username} - {self.level} - Score: {self.score}"

    class Meta:
        ordering = ['-score', '-created_at']  # Order by score and then by creation date


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.created_at}"

# game/models.py

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games_played = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

# game/models.py

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
