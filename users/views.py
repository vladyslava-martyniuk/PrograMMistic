from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        u_form = RegistrationForm(request.POST, request.FILES)

        if u_form.is_valid():
            user = u_form.save(commit=False)

            user.set_password(u_form.cleaned_data['password1'])
            user.save()

            Profile.objects.create(
                user=user,
                bio=u_form.cleaned_data['bio'],
                avatar=u_form.cleaned_data['avatar'],
            )

            login(request, user)
            return redirect('dashboard')

    else:
        u_form = RegistrationForm()

    return render(request, 'register.html', {'u_form': u_form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': user_profile
    })


def user_logout(request):
    logout(request)
    return redirect('login')