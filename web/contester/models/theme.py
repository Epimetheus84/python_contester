from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def all_exercises():
        res = []
        themes = Theme.objects.all()
        for theme in themes:
            theme.exercises = theme.exercise_set.all()
            res.append(theme)

        return res
