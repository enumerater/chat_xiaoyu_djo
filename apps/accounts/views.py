from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register_view(request):
    context = {
        'test': 'test',
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    context = {
        'test': 'test',
    }
    return render(request, 'accounts/login.html', context)
