from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Confession, Comment, Community

class CommunityForm(forms.ModelForm):
    """Form for creating and editing communities."""
    class Meta:
        model = Community
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Community name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Community description'}),
        }

class ConfessionForm(forms.ModelForm):
    """Form for creating and editing confessions."""
    class Meta:
        model = Confession
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your confession...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment...'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
