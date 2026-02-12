from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Experience, Profile, Connection
from .forms import RegistrationForm # Import the form

# Create your views here.
def home(request):
    experiences = Experience.objects.all().order_by('-created_at')
    return render(request, 'wisdom_app/home.html', {'experiences': experiences})

# Registration View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Create a Profile instance for the new user
            Profile.objects.create(user=user)
            login(request, user) # Log the user in after registration
            return redirect('wisdom_app:home') # Redirect to home page
    else:
        form = RegistrationForm()
    return render(request, 'wisdom_app/register.html', {'form': form})

@login_required
def profile(request, username):
    # Basic profile view - needs refinement
    # You would typically fetch the user by username and then their profile
    # profile_user = User.objects.get(username=username)
    # profile_data = Profile.objects.get(user=profile_user)
    # For now, just showing a placeholder
    return render(request, 'wisdom_app/profile.html', {'username': username})

@login_required
def create_experience(request):
    # Placeholder for experience creation form
    return render(request, 'wisdom_app/create_experience.html')

@login_required
def experience_detail(request, pk):
    # Placeholder for viewing a single experience
    # experience = Experience.objects.get(pk=pk)
    return render(request, 'wisdom_app/experience_detail.html', {'pk': pk})

@login_required
def connections(request):
    # Placeholder for connection management
    return render(request, 'wisdom_app/connections.html') 