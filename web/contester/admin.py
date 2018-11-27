from django.contrib import admin
from .models.user import User
from .models.exercise import Exercise
from .models.theme import Theme

# Register your models here.
admin.site.register(User)
admin.site.register(Theme)
admin.site.register(Exercise)
