from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .models import *
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages


def home(request):
    return render(request, 'pages/index.html')
def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

## AUthentication views

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email belongs to an AdminUser
        admin_user = authenticate(request, email=email, password=password)
        if admin_user is not None and isinstance(admin_user, AdminUser):
            login(request, admin_user)
            return redirect('/admin/')  # Redirect Admins to Django Admin Panel

        # Check if the email belongs to a Student
        try:
            student = Student.objects.get(email=email)
            if student.check_password(password):
                login(request, student)
                return redirect('base:student_dashboard')  # Redirect students to their dashboard
            else:
                messages.error(request, "Invalid email or password.")
        except Student.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'pages/auth/login.html')

def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])  # Hash password
            student.status = 'pending'  # Ensure student is pending approval
            student.save()

            # Load email template
            email_subject = "Registration Successful - Pending Approval"
            email_html_content = render_to_string("emails/registration_email.html", {
                "full_name": student.full_name,
            })
            email_text_content = strip_tags(email_html_content)  # Convert to plain text

            # Send email with HTML content
            email = EmailMultiAlternatives(
                subject=email_subject,
                body=email_text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[student.email],
            )
            email.attach_alternative(email_html_content, "text/html")
            email.send()

            return redirect('base:login')  # Redirect to login page after registration

    else:
        form = StudentRegistrationForm()  # Load empty form

    return render(request, 'pages/auth/register.html', {'form': form})


