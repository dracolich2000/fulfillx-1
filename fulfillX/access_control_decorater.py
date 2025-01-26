from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to check if the user's role is in the list of allowed roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user_role = getattr(request.user, 'role', None)
            
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        return wrapper
    return decorator
