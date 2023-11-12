from django import forms
from .models import Komment

class CommentForm(forms.ModelForm):
    comment=forms.CharField(label='Текст комментария',required=True, widget=forms.Textarea(attrs={'rows':3}))
    class Meta:
        model = Komment
        fields = ['comment']
