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

   

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text="Пароль має містити не менше 8 символів.")
    password2 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput, help_text="Повторіть пароль.")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': "Ім'я користувача (логін)",
            'email': 'Електронна пошта',
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
        }
        help_texts = {
            'username': "",
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError("Паролі не збігаються")
            if len(p1) < 8:
                raise forms.ValidationError("Пароль повинен бути не менше 8 символів")
        
        return cleaned_data
