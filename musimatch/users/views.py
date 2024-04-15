from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.

def profile_view(request):
    return render(request, "profile.html")


def register_view(request):
    # redirect for when register form is valid and submitted
    # note: in a valid form, username cannot be existing
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("users:profile")
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", { "form": form })


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("users:profile")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", { "form": form })


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    