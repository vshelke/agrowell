from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'general/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'general/login.html')
    return render(request, 'general/login.html')

def signup_view(request):
    return render(request, 'general/signup.html')

def logout_view(request):
    logout(request)
    return redirect('/')
    