from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    logout,
    login
)
from authentication.forms import UserRegistrationForm, AccountAuthenticationForm

# Create your views here.


def test_register(request):
    return render(request, 'authentication/user_registration.html')


def test_login(request):
    return render(request, 'authentication/login.html')


def user_login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("dashboard")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Login, Please try again...")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'authentication/user_login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect("dashboard")


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("dashboard")
        else:
            print(form.is_valid())
            print(form.errors)
    form = UserRegistrationForm()
    return render(request, 'authentication/user_registration.html', {'form': form})


@login_required(login_url='user_login')
def dashboard(request):
    return render(request, 'authentication/dashboard.html', {})
