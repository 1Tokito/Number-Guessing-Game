from django.contrib import admin

# Register your models here.
# game/admin.py

from django.contrib import admin
from .models import Game, Feedback

class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'attempts', 'score', 'level', 'created_at')
    search_fields = ('user__username', 'level')
    list_filter = ('level',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)

admin.site.register(Game, GameAdmin)
admin.site.register(Feedback, FeedbackAdmin)

# game/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Game, Feedback, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_games_played', 'total_wins', 'best_score')
    search_fields = ('user__username',)

# Register UserProfile with the Django admin
admin.site.register(UserProfile, UserProfileAdmin)

# game/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)

admin.site.unregister(User)  # Unregister the original User admin
admin.site.register(User, UserAdmin)  # Register the new User admin


