from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    score = forms.FloatField(widget=forms.NumberInput(attrs={'max': 10, 'min': 0, 'step': 0.5, 'placeholder':'평점을 남겨주세요.(0.5점 단위로 입력가능합니다.)'}))
    class Meta:
        model = Review
        fields = ('content', 'score', )
        widgets = {
            'content': forms.TextInput(attrs={'maxlength': 100, 'size':72, 'placeholder': '감상평을 남겨주세요.'})
        }