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
    path('logout/', logout_view, name="logout"),  # Logout route

    ##Authentication urls
    path('login/', login_view, name="login"),
    path('register/', register, name='register'),
    ##Admin urls
    path('admin-dashboard/', admin_dashboard, name="admin_dashboard"),
    path('admin-show/', admin_show, name="admin_show"),
    path('approved-students/', approved_students, name="approved_students"),
    path('rejected-students/', rejected_students, name="rejected_students"),
    ##Students urls
    path('student-detail/<int:student_id>/', student_detail, name="student_detail"),
    path('student-dashboard/', home, name="student_dashboard"),
]
