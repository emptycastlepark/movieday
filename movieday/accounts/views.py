from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('accounts:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.profile_image:
                user.save()
            else:
                user.profile_image = '../static/default.jpg'
                user.save()
            # auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    # if request.user.is_authenticated:
    #     return redirect('accounts:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:index')


def update(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if user.profile_image:
                user.save()
            else:
                user.profile_image = '../static/default.jpg'
                user.save()
            # auth_login(request, user)
            return redirect('accounts:detail', user.id)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def detail(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
    }
    return render(request, 'accounts/detail.html', context)
