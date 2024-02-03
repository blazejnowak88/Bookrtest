# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from django import forms

from .models import Publisher, Review, Book




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "book"]

    rating = forms.IntegerField(min_value=0, max_value=5)
