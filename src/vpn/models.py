from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    @property
    def total_transitions(self):
        return sum([site.transitions_count for site in self.sites.all()])

    @property
    def total_data_volume(self):
        return sum([site.data_volume for site in self.sites.all()])

    @property
    def formatted_data_volume(self):
        kb = int(self.total_data_volume) / 1024
        mb = kb / 1024
        gb = mb / 1024

        if gb >= 1:
            return f"{gb:.2f} GB"
        elif mb >= 1:
            return f"{mb:.2f} MB"
        elif kb >= 1:
            return f"{kb:.2f} KB"
        else:
            return f"{self.total_data_volume} Bytes"


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

    @property
    def go_to_site(self):
        return f"{settings.BASE_HOST_URL}{self.name}"

    @property
    def formatted_data_volume(self):
        kb = int(self.data_volume) / 1024
        mb = kb / 1024
        gb = mb / 1024

        if gb >= 1:
            return f"{gb:.2f} GB"
        elif mb >= 1:
            return f"{mb:.2f} MB"
        elif kb >= 1:
            return f"{kb:.2f} KB"
        else:
            return f"{self.data_volume} Bytes"
