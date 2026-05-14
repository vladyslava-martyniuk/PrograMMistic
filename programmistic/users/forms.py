from django import forms
from django.contrib.auth.models import User
from posts.models import Post


class RegistrationForm(forms.ModelForm):
    bio = forms.CharField(
        label='Про себе',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )
    avatar = forms.ImageField(label='Аватар', required=False)

    post = forms.ModelChoiceField(
        queryset=Post.objects.all(),
        label='Оберіть пост',
        required=False,
        empty_label="--- Оберіть пост ---"
    )

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError("Паролі не збігаються")
        return cleaned_data
