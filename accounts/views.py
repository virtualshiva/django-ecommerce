
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . forms import LoginForm
from django.contrib.auth.decorators import login_required
from .auth import admin_only




# Create your views here.



def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'account created successfully')
            return redirect('/register')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form fields')
            return render(request, 'accounts/register.html', {'form':form})

    context = {
        'form': UserCreationForm
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'],password = data['password'])
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                messages.add_message(request, messages.ERROR, 'Plaese provide correect credentials')
                return render(request, 'accounts/login.html', {'form':form})
    context={
        'form':LoginForm
    }
    return render(request, 'accounts/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('/login')

@login_required
@admin_only
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
