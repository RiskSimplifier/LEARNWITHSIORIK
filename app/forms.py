from django import forms

from app.models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review_title','review_content','rating']

class TransactionForm(forms.Form):
    course_code = forms.CharField(max_length=100)