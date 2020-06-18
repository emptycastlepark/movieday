from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from movies.models import Movie

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect('movies:movie_list')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/userform.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:movie_list')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('index')


@login_required
def update(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                person = form.save()
                if not person.profile_image:
                    person.profile_image = '../media/default.jpg'
                    person.save()
                return redirect('accounts:detail', person.id)
        else:
            form = CustomUserChangeForm(instance=user)
        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'accounts/userform.html', context)
    else:
        return redirect('index')

@login_required
def detail(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    reviews = user.moviereview_set.order_by('-created_at')

    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genre_score_dict = dict()

    if len(reviews) > 0:
        for review in reviews:
            for genre in review.movie.genres.all():
                genre_score_dict[genre.name] = genre_score_dict.get(genre.name, []) + [review.score]

    genre_score_average = []
    for genre in genre_score_dict.keys():
        average_score = f'{sum(genre_score_dict[genre])/len(genre_score_dict[genre]):.2f}'
        genre_score_average.append([genre, average_score])

    genre_score_average = sorted(genre_score_average, key=lambda score: float(score[1]), reverse=True)

    context = {
        'user': user,
        'person': request.user,
        'page_obj': page_obj,
        'genre_score_average': genre_score_average,
    }
    return render(request, 'accounts/detail.html', context)


def get_movies(request, user_id, key):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if key == 0:
        movies = list(user.like_movies.all().values())
    elif key == 1:
        movies = list(user.later_movies.all().values())
    elif key == 2:
        movies = list(user.exclude_movies.all().values())

    return JsonResponse({'movies': movies}, status = 200)

def get_reviews(request, user_id, page):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    max_review_page = user.moviereview_set.count() // 10 + 1

    reviews = list(user.moviereview_set.order_by('-created_at').values()[(page-1)*10:page*10])
    review_movies = dict()
    for review in reviews:
        temp_movie = get_object_or_404(Movie, id = review['movie_id'])
        review_movies[temp_movie.id] = temp_movie.title

    return JsonResponse({'reviews': reviews, 'review_movies': review_movies, 'max_review_page': max_review_page}, status = 200)