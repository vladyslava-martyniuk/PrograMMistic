from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст поста',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введіть заголовок'}),
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Введіть текст поста'}),
        }
