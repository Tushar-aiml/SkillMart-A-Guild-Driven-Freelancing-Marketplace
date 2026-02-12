# Register your models here.
from django.contrib import admin
from .models import Profile, Experience, Connection

admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(Connection) 