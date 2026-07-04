from django.contrib import messages
from django.shortcuts import redirect, render

from .decorators import login_required_session
from .forms import LoginForm, RegisterForm
from .hashing import hash_password, verify_password
from .models import CustomUser


def register_view(request):
    if request.session.get("user_id"):
        return redirect("ciphers:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            algorithm = form.cleaned_data["algorithm"]

            if CustomUser.objects.filter(username=username).exists():
                form.add_error("username", "That username is already taken.")
            else:
                hashed = hash_password(password, algorithm)
                CustomUser.objects.create(
                    username=username,
                    password_hash=hashed,
                    hash_algorithm=algorithm,
                )
                messages.success(
                    request,
                    f"Account created for '{username}'. Stored {algorithm.upper()} hash: {hashed}",
                )
                return redirect("accounts:login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.session.get("user_id"):
        return redirect("ciphers:dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                user = None

            if user and verify_password(password, user.password_hash, user.hash_algorithm):
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("ciphers:dashboard")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required_session
def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")
