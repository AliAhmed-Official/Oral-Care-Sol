from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from userauths.forms import UserRegisterForm, ProfileForm
from userauths.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse

#User = settings.AUTH_USER_MODEL

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form .is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, Your account is created successfully.')
            new_user = authenticate(username = form.cleaned_data['User_Email'], password = form.cleaned_data['password1'])
            login(request, new_user)
            Profile.objects.create(user = request.user, full_name = username)
            return redirect('OCS_APP:index')
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request, 'userauths/register.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('OCS_APP:index')
    if request.method == "POST":
        User_Email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(User_Email=User_Email)
            user = authenticate(request, User_Email = User_Email, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in.')
                return redirect('OCS_APP:index')
            else:
                messages.warning(request, 'Invalid email or password. Please try again.')
        except:
            messages.warning(request, 'Invalid email or password. Please try again.')
    return render(request, 'userauths/log-in.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    request.session.flush()
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('userauths:log-in')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_update(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.user = request.user
            new_form.save()
            u = User.objects.get(username = request.user.username)
            u.username = form.cleaned_data['full_name']
            u.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('OCS_APP:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'userauths/profile-edit.html', {'form':form, 'profile':profile})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request):
    return render(request, 'userauths/forgot_password.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_reset_password_email(request):
    email = request.GET.get('email')
    user = User.objects.filter(email=email).first()
    if user is not None:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://127.0.0.1:8000/user/reset/{str(uid)}/{str(token)}/"
        send_mail('Password reset request', f'Click the following link to reset your password: {reset_link}', 'aliahmedchamp@gmail.com', [email], fail_silently=False)
        return JsonResponse({'correct':True})
    else:
        return JsonResponse({'incorrect':False})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                messages.warning(request, 'Passwords do not match.')
                return render(request, 'userauths/password_reset_form.html')
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('userauths:log-in')
        else:
            return render(request, 'userauths/password_reset_form.html', {'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'userauths/password_reset_invalid.html')