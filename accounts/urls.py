from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/<int:user_id>/', views.update, name='update'),
    path('detail/<int:user_id>/', views.detail, name='detail'),
    path('get_movies/<int:user_id>/<int:key>/', views.get_movies, name="get_movies"),
    path('get_reviews/<int:user_id>/<int:page>/', views.get_reviews, name="get_reviews"),
]