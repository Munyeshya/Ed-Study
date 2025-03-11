from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('services', services, name="services"),
    path('contact', contact, name="contact"),
    
    ##Authentication urls
    path('login/', login_view, name="login"),
    path('register/', register, name='register'),
    path('student-dashboard/', home, name="student_dashboard"),
]
