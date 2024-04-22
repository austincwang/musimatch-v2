from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import login, logout, get_user_model
from .forms import RegisterForm, LoginForm, UpdateProfileForm
from django.contrib import messages

# Create your views here.

def profile_view(request, user_name):
    try:
        current_user = get_user_model().objects.get(username=user_name)
        context = {}
        context['username'] = user_name
        context['pfp'] = current_user.pfp.url
        context['description'] = current_user.description
        context['date_joined'] = current_user.date_joined
    except:
        return redirect("/error/user_not_found")
    return render(request, "profile.html", context)


def register_view(request):
    # redirect for when register form is valid and submitted
    # note: in a valid form, username cannot be existing
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("users:profile")
    else:
        form = RegisterForm()
    
    return render(request, "register.html", { "form": form })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            user_name = form.cleaned_data.get("username")
            return redirect("users:profile", user_name = user_name)
    else:
        form = LoginForm()

    return render(request, "login.html", { "form": form })


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    

def edit_profile_view(request):
    if request.method == "POST":
        current_user = get_user_model().objects.get(username=request.user.username)
        form = UpdateProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "Profile updated successfully")
            return redirect("users:profile")
    else:
        form = UpdateProfileForm(instance=request.user)
    
    return render(request, "edit-profile.html", { "form": form })

    