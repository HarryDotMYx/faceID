from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from users.forms import UserRegisterForm
from users.exceptions import UserInactiveError, UserBannedError, InvalidCredentialsError

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False  # User needs activation
            user.save()
            
            # Send activation email (implement this)
            # send_activation_email(user)
            
            messages.success(
                request,
                'Account created successfully! Please check your email to activate your account.'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    try:
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                
                # Check user status
                if not user.is_active:
                    raise UserInactiveError()
                
                if hasattr(user, 'profile') and user.profile.is_banned:
                    raise UserBannedError()
                
                # Reset failed login attempts
                user.profile.reset_failed_login()
                
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('recognition:main:home')
            else:
                # Increment failed login attempts
                if 'username' in form.cleaned_data:
                    try:
                        user = User.objects.get(username=form.cleaned_data['username'])
                        user.profile.increment_failed_login()
                    except User.DoesNotExist:
                        pass
                raise InvalidCredentialsError()
                
    except UserInactiveError as e:
        messages.error(request, str(e))
    except UserBannedError as e:
        messages.error(request, str(e))
    except InvalidCredentialsError as e:
        messages.error(request, str(e))
    
    form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('recognition:main:home')