from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import UserProfile, UserSearch
from autonumbers.models import SearchSubscription

def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("create_search")
        else:
            messages.error(request, "Невірний логін або пароль.")

    return render(request, "auth/auth_form.html", {
        "form": form,
        "title": "Вхід",
        "button_text": "Увійти",
        "is_login": True,
    })


def user_register(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        phone = form.cleaned_data["phone"]
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, phone=phone)
        login(request, user)
        return redirect("create_search")

    elif request.method == "POST":
        messages.error(request, "Форма містить помилки. Перевірте дані.")

    return render(request, "auth/auth_form.html", {
        "form": form,
        "title": "Реєстрація",
        "button_text": "Зареєструватися",
        "is_login": False,
    })


@login_required
def profile_page(request):
    user = request.user
    email_form = ProfileUpdateForm(instance=user)
    password_form = PasswordChangeForm(user)
    success = False

    if request.method == 'POST':
        if 'update_email_phone' in request.POST:
            email_form = ProfileUpdateForm(request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                success = True

        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                success = True

        elif 'clear_search_history' in request.POST:
            UserSearch.objects.filter(user=user).delete()
            success = True

    searches = UserSearch.objects.filter(user=user).order_by('-created_at')
    subscriptions = SearchSubscription.objects.filter(user=user).order_by('-created_at')

    return render(request, 'autonumbers/profile.html', {
        'email_form': email_form,
        'password_form': password_form,
        'searches': searches,
        'success': success,
        'subscriptions': subscriptions,
    })