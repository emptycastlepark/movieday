from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.contrib import messages

from movieday.settings import SECRET_KEY_WEATHER_API_KEY, SECRET_KEY_MOVIE_API_KEY, SECRET_KEY_KOBIS_API_KEY
from .models import Movie, Genre, MovieReview
from .forms import MovieReviewForm, MovieReviewWithoutMovieForm

import random, json

def index(request):
    movie_count = Movie.objects.all().count()
    review_count = MovieReview.objects.all().count()
    context = {
        'movie_count': movie_count,
        'review_count': review_count,
    }
    return render(request, 'movies/index.html', context)

@login_required
def movie_list(request):
    movie_cnt = Movie.objects.exclude(id__in=request.user.exclude_movies.all()).count() // 16
    context = {
        'movie_cnt': movie_cnt
    }
    return render(request, 'movies/movies_list.html', context)

@login_required
def movie_recommend(request):
    user = request.user

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
    return render(request, 'movies/movies_recommend.html', context)


def movie_upcoming(request):
    context = {
        'MOVIE_API_KEY': SECRET_KEY_MOVIE_API_KEY
    }
    return render(request, 'movies/movies_upcoming.html', context)


def review_list(request):
    reviews = MovieReview.objects.order_by('-created_at')

    paginator = Paginator(reviews, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': reviews,
        'page_obj': page_obj,
    }
    return render(request, 'movies/review_list.html', context)

def review_top_movie(request):

    top_movie_totals = MovieReview.objects.values('movie').annotate(total=Avg('score')).order_by('-total')[:3]

    first_movies = MovieReview.objects.values('movie').annotate(total=Avg('score')).order_by('-total')[0]
    second_movies = MovieReview.objects.values('movie').annotate(total=Avg('score')).order_by('-total')[1]
    last_movies = MovieReview.objects.values('movie').annotate(total=Avg('score')).order_by('-total')[2]
    first_movie = Movie.objects.get(id=first_movies['movie'])
    second_movie = Movie.objects.get(id=second_movies['movie'])
    last_movie = Movie.objects.get(id=last_movies['movie'])

    top_movies = [[first_movie, first_movies['total']], [second_movie, second_movies['total']], [last_movie, last_movies['total']]]

    context = {
        'top_movies': top_movies,
    }
    return render(request, 'movies/review_top_movie.html', context)

def review_list_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = MovieReview.objects.filter(movie_id=movie.id).order_by('-created_at')
    paginator = Paginator(reviews, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movie': movie,
        'reviews': reviews,
        'page_obj': page_obj,
    }
    return render(request, 'movies/review_list_movie.html', context)

def review_detail(request, review_id):
    review = get_object_or_404(MovieReview, id=review_id)
    context = {
        'review': review,
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.id in request.user.moviereview_set.all().values_list('movie', flat=True):
        review = movie.moviereview_set.get(author=request.user)
        messages.warning(request, '이미 리뷰를 작성한 영화입니다.', extra_tags=review.id)
        return redirect('movies:review_list')
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            review.save()
            return redirect('movies:review_list')
    else:
        form = MovieReviewForm()
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'movies/review_create.html', context)


@login_required
def review_create_withoutmovie(request):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=request.POST['movie'])
        if movie.id in request.user.moviereview_set.all().values_list('movie', flat=True):
            review = movie.moviereview_set.get(author=request.user)
            messages.warning(request, '이미 리뷰를 작성한 영화입니다.', extra_tags=review.id)
            return redirect('movies:review_list')
        form = MovieReviewWithoutMovieForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('movies:review_list')
    else:
        form = MovieReviewWithoutMovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/review_create.html', context)


def review_update(request, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(MovieReview, id=review_id)
        if request.user == review.author:
            if request.method == 'POST':
                form = MovieReviewForm(request.POST, instance=review)
                if form.is_valid():
                    review = form.save()
                    return redirect('movies:review_detail', review.id)
            else:
                form = MovieReviewForm(instance=review)
            context = {
                'form': form,
                'review': review,
                'movie': review.movie,
            }
            return render(request, 'movies/review_update.html', context)
        else:
            return redirect('movies:review_detail', review.id)
    else:
        return redirect('accounts:login')


def review_delete(request, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(MovieReview, id=review_id)
        if request.user == review.author and request.method=='POST':
            movie_id = review.movie.id
            review.delete()
            return redirect('movies:review_list_movie', movie_id)
        else:
            return redirect('movies:review_detail', review.id)
    else:
        return redirect('accounts:login')


def get_movies(request, pageNum, key, genre_key):
    like_movies = list(request.user.like_movies.values_list('id', flat=True))
    exclude_movies = list(request.user.exclude_movies.values_list('id', flat=True))
    later_movies = list(request.user.later_movies.values_list('id', flat=True))
    genre_name = [None, 'Adventure', 'Fantasy', 'Animation', 'Drama', 'Horror', 'Action', 'Comedy', 'Western', 'Thriller', 'Crime', 'Documentary', 'Science Fiction',
                'Mystery', 'Music', 'Romance', 'Family', 'War', 'History', 'TV Movie']

    if genre_key == 0:
        genre_movies = Movie.objects.exclude(id__in=request.user.exclude_movies.all())
    else:
        genre_movies = Genre.objects.get(name=genre_name[genre_key]).movie_set.exclude(id__in=request.user.exclude_movies.all())

    if key == 0:
        movies = list(genre_movies.order_by('-vote_average').values())[pageNum*16:(pageNum+1)*16]
    elif key == 1:
        movies = list(genre_movies.order_by('-release_date').values())[pageNum*16:(pageNum+1)*16]

    max_page = len(genre_movies) // 16
    if len(genre_movies) % 16 == 0:
        max_page -= 1

    return JsonResponse({'movies': movies, 'like_movies': like_movies, 'exclude_movies': exclude_movies, 'later_movies': later_movies, 'max_page': max_page}, status = 200)

def search_movies(request, searchInput, pageNum):
    entire_movies = list(Movie.objects.filter(Q(title__contains=searchInput) | Q(original_title__contains=searchInput)).values())

    max_page = len(entire_movies) // 16
    if len(entire_movies) % 16 == 0:
        max_page -= 1

    movies = entire_movies[pageNum*16:(pageNum+1)*16]
    
    print(searchInput)
    return JsonResponse({'movies': movies, 'max_page': max_page}, status = 200)


def get_genres(request, movie_id):
    genres = list(get_object_or_404(Movie, id=movie_id).genres.all().values_list('name', flat=True))
    return JsonResponse({'genres': genres}, status = 200)

def get_reviews(request, movie_id):
    reviews = list(get_object_or_404(Movie, id=movie_id).moviereview_set.all().order_by('-created_at')[:5].values_list('content', flat=True))
    return JsonResponse({'reviews': reviews}, status = 200)

def make_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie_reviews = movie.moviereview_set.all()

    form = MovieReviewForm()

    review = form.save(commit=False)
    review.content = request.GET.get('content')
    review.score = request.GET.get('score')
    review.author = request.user
    review.movie = movie

    exist_review = None
    if movie_reviews.filter(id__in=request.user.moviereview_set.all()).exists():
        result = "exist"
        exist_review = movie_reviews.get(author=request.user).id
    elif len(request.GET.get('content')) <= 50:
        review.save()
        result = "success"
    else:
        result = "false"

    review = review.serializable_value('content')

    return JsonResponse({'review': review, 'result': result, 'exist_review': exist_review}, status = 200)


def get_movie_recommend(request, weather, temp):
    recommend_genre = []

    if (float(temp) < 0):
        recommend_genre.append(["날씨가 매우 춥네요~, ", ["Science Fiction", "War"]])
    elif (0 <= float(temp) < 5):
        recommend_genre.append(["겨울이 다가오는 것 같군요, ", ["Fantasy", "Animation"]])
    elif (5 <= float(temp) < 10):
        recommend_genre.append(["날씨가 제법 쌀쌀하군요, ", ["Drama", "Comedy"]])
    elif (10 <= float(temp) < 15):
        recommend_genre.append(["조금 쌀쌀하지만 시원한 날씨입니다. ", ["Crime", "Mystery"]])
    elif (15 <= float(temp) < 20):
        recommend_genre.append(["날씨가 시원하네요~, ", ["Romance", "Music"]])
    elif (20 <= float(temp) < 25):
        recommend_genre.append(["야외활동하기 매우 좋은 날씨입니다. ", ["Adventure", "Action", "Western"]])
    elif (25 <= float(temp) < 30):
        recommend_genre.append(["여름이 다가오는 것 같군요, ", ["Documentary", "Family"]])
    elif (30 <= float(temp)):
        recommend_genre.append(["날씨가 덥네요~, ", ["Horror", "Thriller"]])

    if (weather == "Thunderstorm"):
        recommend_genre.append(["천둥번개 치는 날, ", ["Horror", "Thriller"]])
    elif (weather == "Drizzle"):
        recommend_genre.append(["이슬비가 내리는 날, ", ["Drama", "Music"]])
    elif (weather == "Rain"):
        recommend_genre.append(["비가 많이 내리는 날, ", ["Crime", "Thriller"]])
    elif (weather == "Snow"):
        recommend_genre.append(["눈이 내리는 날, ", ["Romance", "Fantasy"]])
    elif (weather == "Mist"):
        recommend_genre.append(["안개가 옅게 낀 날, ", ["Mystery", "Music"]])
    elif (weather == "Haze"):
        recommend_genre.append(["먼지가 많고 흐린 날, ", ["Documentary", "Science Fiction"]])
    elif (weather == "Dust"):
        recommend_genre.append(["먼지가 많은 날, ", ["Adventure", "Western"]])
    elif (weather == "Fog"):
        recommend_genre.append(["안개가 짙은 날, ", ["Crime", "Mystery"]])
    elif (weather == "Squall"):
        recommend_genre.append(["바람이 강한 날, ", ["Adventure", "War"]])
    elif (weather == "Tornado"):
        recommend_genre.append(["태풍부는 날, ", ["Documentary", "Science Fiction"]])
    elif (weather == "Clear"):
        recommend_genre.append(["맑은 날, ", ["Romance", "Family"]])
    elif (weather == "Clouds"):
        recommend_genre.append(["구름낀 날,", ["Animation", "Family"]])
    elif (weather == "Smoke"):
        recommend_genre.append(["구름이 짙은 날, ", ["Drama", "Action"]])
    elif (weather == "Sand"):
        recommend_genre.append(["황사가 부는 날, ", ["Western", "War"]])
    elif (weather == "Ash"):
        recommend_genre.append(["매우 흐린 날, ", ["Comedy", "Action"]])

    final_recommend = random.choice(recommend_genre)

    final_reason = final_recommend[0]
    final_genre = random.choice(final_recommend[1])
    
    recommended_movies = list(Genre.objects.get(name=final_genre).movie_set.exclude(id__in=request.user.exclude_movies.all()).values())[:18]

    return JsonResponse({'final_reason': final_reason, 'final_genre': final_genre, 'recommended_movies': recommended_movies}, status = 200)


def movie_like(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': movie.like_users.count()})

def movie_exclude(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.exclude_users.filter(pk=user.pk).exists():
        movie.exclude_users.remove(user)
        exclude = False
    else:
        movie.exclude_users.add(user)
        exclude = True

    return JsonResponse({'exclude': exclude})

def movie_later(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.later_users.filter(pk=user.pk).exists():
        movie.later_users.remove(user)
        later = False
    else:
        movie.later_users.add(user)
        later = True

    return JsonResponse({'later': later})

@register.filter
def helper_function(input_list):

    slicing_list = list(input_list)
    sliced_list = []

    for i in range(1, len(slicing_list) // 6):
        sliced_list.append(slicing_list[6*i:6*(i+1)])

    return sliced_list

