from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .models import *
from django.contrib.auth import login


def home(request):
    return render(request, 'pages/index.html')
def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

## AUthentication views

def login(request):
    return render(request, 'pages/auth/login.html')
def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])  # Hash password
            student.status = 'pending'  # Ensure student is pending approval
            student.save()

            return redirect('register_success')  # Redirect to success page

    else:
        form = StudentRegistrationForm()  # Load empty form

    return render(request, 'pages/auth/register.html', {'form': form})

def register_success(request):
    return render(request, 'pages/auth/register_success.html')
