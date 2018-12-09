from django.db import models
from .exercise import Exercise
from .user import User


class Test(models.Model):
    successfully = models.BooleanField()
    message = models.CharField(max_length=50)
    exercise = models.ForeignKey(Exercise, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return self.message
