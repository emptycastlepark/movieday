from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/<int:user_id>', views.update, name='update'),
    path('detail/<int:user_id>', views.detail, name='detail'),
]