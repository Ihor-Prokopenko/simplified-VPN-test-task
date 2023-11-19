from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=100)
    base_url = models.URLField()
    transitions_count = models.IntegerField(default=0)
    data_volume = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def add_transition(self):
        self.transitions_count += 1

    def remove_transition(self):
        self.transitions_count -= 1
