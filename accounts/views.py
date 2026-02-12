from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    """Extend the default user creation form with required email and validation."""

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        service_type = request.POST.get("service_type") or ""
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                service_type=service_type,
            )
            messages.success(request, "Account created. Please log in.")
            return redirect("accounts:login")
    else:
        form = RegistrationForm()
    # Preserve the selected service_type when re-rendering the form on errors
    context = {"form": form, "service_type": request.POST.get("service_type", "")}
    return render(request, "accounts/register.html", context)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Ensure user has completed their profile; if not, redirect to profile edit
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user)

            incomplete = not (profile.location and profile.skills)
            if incomplete:
                messages.info(request, "Please complete your profile before continuing.")
                return redirect("accounts:profile")

            return redirect("accounts:dashboard")
        else:
            # Provide a friendly, non-revealing error message for failed login
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("accounts:login")


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    profile = UserProfile.objects.get(user=request.user)
    return render(request, "accounts/dashboard.html", {"profile": profile})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        profile.skills = request.POST.get("skills", profile.skills)
        profile.location = request.POST.get("location", profile.location)
        profile.bio = request.POST.get("bio", profile.bio)
        profile.service_type = request.POST.get("service_type", profile.service_type)
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"profile": profile})

