from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=10, default="익명")
    profile_image = models.ImageField(upload_to='profile', default='default.jpg')

    like_genres = models.ManyToManyField(Genre, related_name='genre_like_users', blank=True)

    like_movies = models.ManyToManyField(Movie, related_name='like_users', blank=True)
    exclude_movies = models.ManyToManyField(Movie, related_name='exclude_users', blank=True)
    later_movies = models.ManyToManyField(Movie, related_name='later_users', blank=True)