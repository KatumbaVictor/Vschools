from django import forms
from main.models import posts

class new_posts(forms.ModelForm):
    class Meta:
        model = posts
        fields = ['file_uploaded','caption']