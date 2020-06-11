from django.shortcuts import render
from .models import Movie, Genre
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.template.defaulttags import register

# Create your views here.
def index(request):
    movies = Movie.objects.all()

    genres = list(Genre.objects.all())

    genre_dict = dict()
    for genre in genres:
        genre_dict[genre.name] = list(Genre.objects.get(name=genre).movie_set.all())

    genre_cnt = dict()
    for genre in genres:
        genre_cnt[genre.name] = list(range(1, len(genre_dict[genre.name]) // 6))

    # paginator = Paginator(movies, 16)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    print(genre_dict)
    context = {
        'genre_dict': genre_dict,
        'genre_cnt': genre_cnt,
    }
    return render(request, 'movies/index.html', context)



@register.filter
def helper_function(input_list):
    temp_list = []
    for i in range(1, len(input_list)//6):
        temp_list.append(input_list[6*i:6*(i+1)])
    if len(temp_list) > 5:
        temp_list = temp_list[:5]
    return temp_list