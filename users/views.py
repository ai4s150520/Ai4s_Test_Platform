from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import re


User = get_user_model()

def login_register_view(request):
    """
    Handles both user login and registration using the active user model.
    """
    
    if request.method == 'POST':
        # --- REGISTRATION LOGIC ---
        if 'password2' in request.POST:
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            # --- All validation checks remain the same ---
            if not all([username, email, password, password2]):
                messages.error(request, 'All registration fields are required.')
                return redirect('users:login_register')

            if password != password2:
                messages.error(request, 'Passwords do not match. Please try again.')
                return redirect('users:login_register')

            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('users:login_register')

            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                messages.error(request, 'Please enter a valid email address.')
                return redirect('users:login_register')

            # The `User` variable now correctly refers to your CustomUser model
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, f'The username "{username}" is already taken.')
                return redirect('users:login_register')

            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, f'An account with the email "{email}" already exists.')
                return redirect('users:login_register')
            
            # This will now correctly call the manager on your CustomUser model
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, f'Welcome, {username}! Your account has been created. Please log in.')
                return redirect('users:login_register')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred during registration: {e}')
                return redirect('users:login_register')

        # --- LOGIN LOGIC ---
        elif 'identifier' in request.POST:
            identifier = request.POST.get('identifier', '').strip()
            password = request.POST.get('password')

            if not identifier or not password:
                messages.error(request, 'Please provide both your identifier and password.')
                return redirect('users:login_register')
            
            user = None
            try:
                # The `User` variable now correctly refers to your CustomUser model
                if '@' in identifier:
                    user_obj = User.objects.get(email__iexact=identifier)
                    user = authenticate(request, username=user_obj.username, password=password)
                else:
                    user = authenticate(request, username=identifier, password=password)
            except User.DoesNotExist:
                pass
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'core:dashboard') 
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials. Please check your details and try again.')
                return redirect('users:login_register')

    return render(request, 'users/login_register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('users:login_register')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('users:login')
    return redirect('users:profile')

@login_required
def change_password(request):
    if request.method == "POST":
        current = request.POST.get('current_password')
        new1 = request.POST.get('new_password1')
        new2 = request.POST.get('new_password2')

        if not request.user.check_password(current):
            messages.error(request, "Current password is incorrect.")
            return redirect('users:profile')
        if new1 != new2:
            messages.error(request, "New passwords do not match.")
            return redirect('users:profile')
        if not new1 or len(new1) < 8:
            messages.error(request, "New password must be at least 8 characters.")
            return redirect('users:profile')

        request.user.set_password(new1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Password changed successfully.")
        return redirect('users:profile')
    else:
        return redirect('users:profile')