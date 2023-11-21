from django.contrib import admin

from .models import Site, User


admin.site.register(Site)
admin.site.register(User)
