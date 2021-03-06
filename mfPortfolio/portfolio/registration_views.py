from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home_request(request, template_name='guest/home.html'):
    return render(request, template_name)


def signup_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('portfolio')
        else:
            return render(request, 'registration/signup.html', {'form': form})

    form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
