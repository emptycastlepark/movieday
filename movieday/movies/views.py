from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from movieday.settings import SECRET_KEY_WEATHER_API_KEY, SECRET_KEY_MOVIE_API_KEY
from .models import Movie, Genre, MovieReview
from .forms import MovieReviewForm, MovieReviewWithoutMovieForm

import random
import json

def index(request):
    return render(request, 'movies/index.html')

def cardlist(request):
    movie_cnt = Movie.objects.all().count() // 16
    context = {
        'movie_cnt': movie_cnt
    }
    return render(request, 'movies/cardlist.html', context)


def movierec(request):
    user = request.user

    recommend_genre = '평점'
    recommend_movies = Movie.objects.order_by('-vote_average', '-release_date')[:18]

    if user.like_movies.exists() or user.like_genres.exists():
        genres_cnt = dict()

        for movie in user.like_movies.all():
            for genre in movie.genres.all():
                genres_cnt[genre.name] = genres_cnt.get(genre.name, 0) + 1

        for genre in user.like_genres.all():
            genres_cnt[genre.name] = genres_cnt.get(genre.name, 0) + 1

        max_genres = []
        if genres_cnt:
            max_cnt = max(genres_cnt.values())
        else:
            max_cnt = 0

        for genre, cnt in genres_cnt.items():
            if cnt == max_cnt:
                max_genres.append(genre)

        while True:
            recommend_genre = random.choice(max_genres)
            reason = 1
            if Genre.objects.get(name=recommend_genre).movie_set.exclude(id__in=user.like_movies.all()).exclude(id__in=user.exclude_movies.all()).exclude(id__in=user.later_movies.all()).order_by('-vote_average', '-release_date'):
                break
            else:
                max_genres.remove(recommend_genre)
                if not max_genres:
                    recommend_genre = random.choice(Genre.objects.exclude(name="TV Movie").exclude(name="History"))
                    reason = 2
                    break
    else:
        recommend_genre = random.choice(Genre.objects.exclude(name="TV Movie").exclude(name="History"))
        reason = 3

    recommend_movies_genre = Genre.objects.get(name=recommend_genre).movie_set.exclude(id__in=user.like_movies.all()).exclude(id__in=user.exclude_movies.all()).exclude(id__in=user.later_movies.all()).order_by('-vote_average', '-release_date')[:18]

    recommend_movies_score = Movie.objects.all().exclude(id__in=user.like_movies.all()).exclude(id__in=user.exclude_movies.all()).exclude(id__in=user.later_movies.all()).order_by('-vote_average', '-release_date')[:18]

    context = {
        'recommend_genre': recommend_genre,
        'reason': reason,
        'recommend_movies_genre': recommend_movies_genre,
        'recommend_movies_score': recommend_movies_score,
        'WEATHER_API_KEY': SECRET_KEY_WEATHER_API_KEY
    }
    return render(request, 'movies/movierec.html', context)


def upcomingmovies(request):
    context = {
        'MOVIE_API_KEY': SECRET_KEY_MOVIE_API_KEY
    }
    return render(request, 'movies/upcomingmovies.html', context)


@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            review.save()
            return redirect('movies:reviewlist')
    else:
        form = MovieReviewForm()
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'movies/createreview.html', context)


@login_required
def createreviewwithoutmovie(request):
    if request.method == 'POST':
        form = MovieReviewWithoutMovieForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('movies:reviewlist')
    else:
        form = MovieReviewWithoutMovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/createreview.html', context)


def reviewlist(request):
    reviews = MovieReview.objects.order_by('-id')

    paginator = Paginator(reviews, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': reviews,
        'page_obj': page_obj,
    }
    return render(request, 'movies/reviewlist.html', context)


def jsonresponsetest(request, pageNum):
    like_movies = list(request.user.like_movies.values_list('id', flat=True))
    exclude_movies = list(request.user.exclude_movies.values_list('id', flat=True))
    later_movies = list(request.user.later_movies.values_list('id', flat=True))
    movies = list(Movie.objects.exclude(id__in=request.user.exclude_movies.all()).values())[pageNum*16:(pageNum+1)*16]
    return JsonResponse({'movies': movies, 'like_movies': like_movies, 'exclude_movies': exclude_movies, 'later_movies': later_movies}, status = 200)


def getgenres(request, movie_id):
    genres = list(get_object_or_404(Movie, id=movie_id).genres.all().values_list('name', flat=True))
    return JsonResponse({'genres': genres}, status = 200)


def getrecommend(request, weather, temp):
    recommend_genre = []
    if (float(temp) >= 25):
        recommend_genre.append(["오늘 같이 더운 날, ", ["Horror", "Thriller"]])
    if (weather == "Clouds"):
        recommend_genre.append(["흐린 날엔 ", ["Crime", "Mystery"]])

    final_recommend = random.choice(recommend_genre)

    final_reason = final_recommend[0]
    final_genre = random.choice(final_recommend[1])

    return JsonResponse({'final_reason': final_reason, 'final_genre': final_genre}, status = 200)


def like(request, movie_id):
    print(1)
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': movie.like_users.count()
    })

def exclude(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.exclude_users.filter(pk=user.pk).exists():
        movie.exclude_users.remove(user)
        exclude = False
    else:
        movie.exclude_users.add(user)
        exclude = True

    return JsonResponse({
        'exclude': exclude,
    })

def later(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.later_users.filter(pk=user.pk).exists():
        movie.later_users.remove(user)
        later = False
    else:
        movie.later_users.add(user)
        later = True

    return JsonResponse({
        'later': later,
    })

@register.filter
def helper_function(input_list):

    temp_list2 = list(input_list)
    temp_list = []

    for i in range(1, len(temp_list2) // 6):
        temp_list.append(temp_list2[6*i:6*(i+1)])

    return temp_list



def testing(request):
    context = {
        'MOVIE_API_KEY': SECRET_KEY_MOVIE_API_KEY
    }
    return render(request, 'movies/testing.html', context)