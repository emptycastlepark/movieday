from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    movies = Movie.objects.all()

    paginator = Paginator(movies, 16)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies': movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/index.html', context)