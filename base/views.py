from django.shortcuts import render

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
    return render(request, 'pages/auth/register.html')
