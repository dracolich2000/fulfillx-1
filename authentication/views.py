from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from .models import StaffUser
import re

# Create your views here.

def signup(request):
    PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            error = 'Passwords do not match!'
        elif not re.match(PASSWORD_REGEX, password1):
            error = 'Password must be at least 8 characters long and contain both letters and numbers'
        elif len(password1)<8:
            error = 'Password is too short!'
        elif not username or not email or not password1:
            error = 'All fields are required!'
        else:
            role = 'User'

            try:
                user = StaffUser.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password1),
                    role=role
                )
                user.save()
                return redirect('signup_successful')
            
            except Exception as e:
                error = f'An error occurred: {str(e)}'
                print(error)
                return render(request, 'authentication/signup.html',{'error':error})
        return render(request, 'authentication/signup.html',{'error':error})
    return render(request, 'authentication/signup.html')

def signup_successful(request):
    return render(request, 'authentication/signup_successful.html')

def usr_login(request):
    if 'next' in request.GET and not request.user.is_authenticated:
        return redirect('session_expired')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            role = user.role

            if role == 'Admin':
                return redirect('admin_dashboard')
            elif role == 'Staff':
                return redirect('staff_dashboard')
            elif role == 'Vendor':
                return redirect('vendor_dashboard')
            else:
                return redirect('usr_dashboard')
        else:
            error = 'Invalid username or password!'
            return render(request, 'authentication/login.html',{'error':error})
    
    return render(request, 'authentication/login.html')

def usr_logout(request):
    logout(request)
    return redirect('login')

def session_expired(request):
    return render(request, 'authentication/session_expired.html')