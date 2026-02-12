from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'wisdom_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('create/', views.create_experience, name='create_experience'),
    path('experience/<int:pk>/', views.experience_detail, name='experience_detail'),
    path('connections/', views.connections, name='connections'),

    # Basic Auth URLs (Login/Logout)
    # Note: You'll need templates for these (e.g., registration/login.html)
    path('login/', auth_views.LoginView.as_view(template_name='wisdom_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='wisdom_app:home'), name='logout'),
    # Add path for registration view when created
    # path('register/', views.register, name='register'),
    path('register/', views.register, name='register'),
] 