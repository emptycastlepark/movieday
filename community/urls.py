from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.article_index, name='article_index'),
    path('recommend/', views.article_index_recommend, name='article_index_recommend'),
    path('article_create/', views.article_create, name='article_create'),
    path('<int:article_pk>/article_detail/', views.article_detail, name='article_detail'),
    path('<int:article_pk>/article_delete', views.article_delete, name='article_delete'),
    path('<int:article_pk>/article_update', views.article_update, name='article_update'),
    path('<int:article_pk>/article_like/', views.article_like, name='article_like'),
    path('article_search/', views.article_search, name='article_search'),
    path('<int:article_pk>/comment', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]