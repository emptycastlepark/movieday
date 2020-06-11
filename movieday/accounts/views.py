from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:cardlist')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:cardlist')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/userform.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('movies:cardlist')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:cardlist')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('movies:cardlist')


@login_required
def update(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                person = form.save()
                # auth_login(request, person)
                if not person.profile_image:
                    person.profile_image = '../media/default.jpg'
                    person.save()
                return redirect('accounts:detail', person.id)
        else:
            form = CustomUserChangeForm(instance=user)
        context = {
            'form': form,
        }
        return render(request, 'accounts/userform.html', context)
    else:
        return redirect('movies:cardlist')

@login_required
def detail(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
    }
    return render(request, 'accounts/detail.html', context)
