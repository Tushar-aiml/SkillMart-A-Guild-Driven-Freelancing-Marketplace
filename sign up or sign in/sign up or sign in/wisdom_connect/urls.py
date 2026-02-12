"""
URL configuration for wisdom_connect project.

[...] (Django default comments)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wisdom_app.urls')), # Include app URLs
]