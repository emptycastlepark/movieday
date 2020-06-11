from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Genre

class CustomUserCreationForm(UserCreationForm):
    # like_genres = ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False, widget=CheckboxSelectMultiple, label='선호 장르')

    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'profile_image']
        
class CustomUserChangeForm(UserChangeForm):
    like_genres = ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False, widget=CheckboxSelectMultiple, label='선호 장르')
    password = None

    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'like_genres', 'profile_image']
        exclude = ['password']