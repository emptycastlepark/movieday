from django import forms
from .models import MovieReview

class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['content']



class MovieReviewWithoutMovieForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['content', 'movie']