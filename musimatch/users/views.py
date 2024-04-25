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
    if request.user.is_authenticated:
        return redirect("users:profile", user_name = request.user.username)
    
    elif request.method == "POST":
        if 'register_form' in request.POST:
            if request.POST['reg_password1'] != request.POST['reg_password2']:
                messages.error(request, "Passwords do not match")
                return redirect("users:register")
            else:
                register_form = RegisterForm(
                    data = {
                        'username': request.POST['reg_username'],
                        'email': request.POST['reg_email'],
                        'password1': request.POST['reg_password1'],
                        'password2': request.POST['reg_password2']
                    }
                )
                if register_form.is_valid():
                    login(request, register_form.save())
                    messages.success(request, "Account created successfully")
                    user_name = register_form.cleaned_data.get("username")
                    return redirect("users:profile", user_name = user_name)
                else:
                    messages.error(request, "An error occurred")
                    return redirect("users:register")

    return render(request, "register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile", user_name = request.user.username)
    
    elif request.method == "POST":
        if 'login_form' in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                user_name = login_form.cleaned_data.get("username")
                return redirect("users:profile", user_name = user_name)
            else:
                messages.error(request, "User not found")
                return redirect("users:login")
            
        elif 'register_form' in request.POST:
            if request.POST['reg_password1'] != request.POST['reg_password2']:
                messages.error(request, "Passwords do not match")
                return redirect("users:login")
            else:
                register_form = RegisterForm(
                    data = {
                        'username': request.POST['reg_username'],
                        'email': request.POST['reg_email'],
                        'password1': request.POST['reg_password1'],
                        'password2': request.POST['reg_password2']
                    }
                )
                if register_form.is_valid():
                    login(request, register_form.save())
                    messages.success(request, "Account created successfully")
                    user_name = register_form.cleaned_data.get("username")
                    return redirect("users:profile", user_name = user_name)
                else:
                    messages.error(request, "An error occurred")
                    return redirect("users:login")

    return render(request, "login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    

def edit_profile_view(request):
    current_user = get_user_model().objects.get(username=request.user.username)
    
    if request.method == "POST":
        if 'update' in request.POST:
            form = UpdateProfileForm(
                data = {
                    'username': request.POST['username'],
                    'pfp': request.FILES['image'],
                    'description': request.POST['description']
                },
                instance=current_user
            )
            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, "Profile updated successfully")
                return redirect("users:profile", user_name = current_user.username)
            
        elif 'cancel' in request.POST:
            return redirect("users:profile", user_name = current_user.username)
        
    else:
        form = UpdateProfileForm(instance=current_user)

    return render(request, "edit-profile.html")

    