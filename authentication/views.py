from django.shortcuts import render

# Create your views here.


def user_login(request):
    return render(request, 'authentication/user_login.html')


def user_registration(request):
    return render(request, 'authentication/user_registration.html')
