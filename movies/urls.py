from django.urls import path
from . import views

app_name="movies"
urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie_recommend/', views.movie_recommend, name='movie_recommend'),
    path('movie_upcoming/', views.movie_upcoming, name='movie_upcoming'),

    path('review_top_movie/', views.review_top_movie, name='review_top_movie'),
    path('review_list/', views.review_list, name='review_list'),
    path('review_list_movie/<int:movie_id>/', views.review_list_movie, name="review_list_movie"),
    path('review/<int:review_id>/', views.review_detail, name="review_detail"),
    path('review_create_withoutmovie/', views.review_create_withoutmovie, name='review_create_withoutmovie'),
    path('review_create/<int:movie_id>/', views.review_create, name='review_create'),
    path('review_update/<int:review_id>/', views.review_update, name="review_update"),
    path('review_delete/<int:review_id>/', views.review_delete, name="review_delete"),

    path('movie_like/<int:movie_id>/', views.movie_like, name='movie_like'),
    path('movie_exclude/<int:movie_id>/', views.movie_exclude, name='movie_exclude'),
    path('movie_later/<int:movie_id>/', views.movie_later, name='movie_later'),

    path('get_movies/<int:pageNum>/<int:key>/<int:genre_key>/', views.get_movies, name='get_movies'),
    path('search_movies/<str:searchInput>/<int:pageNum>/', views.search_movies, name='search_movies'),

    path('get_genres/<int:movie_id>/', views.get_genres, name='get_genres'),
    path('get_reviews/<int:movie_id>/', views.get_reviews, name='get_reviews'),
    path('make_review/<int:movie_id>/', views.make_review, name='make_review'),
    path('get_movie_recommend/<str:weather>/<str:temp>/', views.get_movie_recommend, name='get_movie_recommend'),

]