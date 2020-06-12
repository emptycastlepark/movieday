from django.urls import path
from . import views

app_name="movies"
urlpatterns = [
    path('', views.cardlist, name='cardlist'),
    path('movierec/', views.movierec, name='movierec'),
    path('upcomingmovies/', views.upcomingmovies, name='upcomingmovies'),

    path('createreview/', views.createreviewwithoutmovie, name='createreviewwithoutmovie'),
    path('createreview/<int:movie_id>/', views.createreview, name='createreview'),
    path('reviewlist/', views.reviewlist, name='reviewlist'),

    path('like/<int:movie_id>/', views.like, name='like'),
    path('exclude/<int:movie_id>/', views.exclude, name='exclude'),
    path('later/<int:movie_id>/', views.later, name='later'),

    path('jsonresponsetest/<int:pageNum>/', views.jsonresponsetest, name='jsonresponsetest'),
    path('getgenres/<int:movie_id>/', views.getgenres, name='getgenres'),
    path('getrecommend/<str:weather>/<str:temp>/', views.getrecommend, name='getrecommend'),

    path('testing/', views.testing, name='testing'),
]