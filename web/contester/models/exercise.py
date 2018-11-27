from django.db import models
from .theme import Theme


class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    input = models.TextField(verbose_name="Input (separated by semicolon)")
    output = models.TextField(verbose_name="Output (separated by semicolon)")
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    maximum_time = models.FloatField(verbose_name="Maximum time of execution")

    def __str__(self):
        return self.name
