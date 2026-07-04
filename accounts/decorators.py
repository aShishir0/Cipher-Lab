from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def login_required_session(view_func):
    """Simple session-based login guard (this project doesn't use Django's
    built-in auth system since passwords are hashed/verified manually)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.warning(request, "Please log in to continue.")
            return redirect("accounts:login")
        return view_func(request, *args, **kwargs)

    return wrapper
