from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from movieday.settings import SECRET_KEY_WEATHER_API_KEY, SECRET_KEY_MOVIE_API_KEY
from .models import Movie, Genre

import json

def index(request):
    return render(request, 'movies/index.html')

def cardlist(request):
    movies = Movie.objects.all()

    paginator = Paginator(movies, 16)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'movies/cardlist.html', context)


def cardlist2(request):
    
    movie_cnt = Movie.objects.all().count() // 16
    context = {
        'movie_cnt': movie_cnt
    }
    return render(request, 'movies/cardlist2.html', context)


def movierec(request):
    import random
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

        recommend_genre = random.choice(max_genres)
        recommend_movies_genre = Genre.objects.get(name=recommend_genre).movie_set.exclude(id__in=user.like_movies.all()).exclude(id__in=user.exclude_movies.all()).exclude(id__in=user.later_movies.all()).order_by('-vote_average', '-release_date')[:18]

    recommend_movies_score = Movie.objects.all().exclude(id__in=user.like_movies.all()).exclude(id__in=user.exclude_movies.all()).exclude(id__in=user.later_movies.all()).order_by('-vote_average', '-release_date')[:18]

    context = {
        'reason': recommend_genre,
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


def jsonresponsetest(request, pageNum):
    like_movies = list(request.user.like_movies.values_list('id', flat=True))
    exclude_movies = list(request.user.exclude_movies.values_list('id', flat=True))
    later_movies = list(request.user.later_movies.values_list('id', flat=True))
    movies = list(Movie.objects.all().values())[pageNum*16:(pageNum+1)*16]
    return JsonResponse({'movies': movies, 'like_movies': like_movies, 'exclude_movies': exclude_movies, 'later_movies': later_movies}, status = 200)


def getgenres(request, movie_id):
    genres = list(get_object_or_404(Movie, id=movie_id).genres.all().values_list('name', flat=True))
    return JsonResponse({'genres': genres}, status = 200)


@register.filter
def helper_function(input_list):

    temp_list2 = list(input_list)
    temp_list = []

    for i in range(1, len(temp_list2) // 6 + 1):
        temp_list.append(temp_list2[6*i:6*(i+1)])

    if len(temp_list) > 5:
        temp_list = temp_list[:5]

    return temp_list