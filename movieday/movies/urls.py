from django.urls import path
from . import views

app_name="movies"
urlpatterns = [
    path('', views.cardlist, name='cardlist'),
    path('testing/', views.cardlist2, name='cardlist2'),
    path('movierec/', views.movierec, name='movierec'),
    path('upcomingmovies/', views.upcomingmovies, name='upcomingmovies'),
    path('jsonresponsetest/<int:pageNum>', views.jsonresponsetest, name='jsonresponsetest'),
    path('getgenres/<int:movie_id>', views.getgenres, name='getgenres'),
]