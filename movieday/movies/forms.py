from django import forms
from .models import MovieReview


SCORE_CHOICES = (('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10))
class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['content', 'score']
        widgets = {
            'score': forms.Select(choices=SCORE_CHOICES)
        }


class MovieReviewWithoutMovieForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['content', 'movie', 'score']
        widgets = {
            'score': forms.Select(choices=SCORE_CHOICES)
        }