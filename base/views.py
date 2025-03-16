from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def home(request):
    return render(request, 'pages/index.html')
def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

def logout_view(request):
    logout(request)  # Log the user out
    return redirect('base:login')  # Redirect to login page

def admin_show(request):
    students = Student.objects.filter(status='pending')

    # Calculate age in whole years
    today = date.today()
    for student in students:
        if student.dob:
            student.age = today.year - student.dob.year  # Only subtract years
        else:
            student.age = "N/A"  # If DOB is missing

    # Add Pagination (10 students per page)
    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    students = paginator.get_page(page_number)

    return render(request, 'pages/admin/show.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Calculate age
    if student.dob:
        today = date.today()
        student.age = today.year - student.dob.year - ((today.month, today.day) < (student.dob.month, student.dob.day))
    else:
        student.age = "N/A"

    return render(request, 'pages/admin/student_detail.html', {'student': student})



## AUthentication views

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Redirect Admins to Admin Dashboard
            if isinstance(user, AdminUser):
                return redirect('base:admin_dashboard')

            # Redirect Students to Student Dashboard
            return redirect('base:student_dashboard')

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'pages/auth/login.html')

@login_required
def admin_dashboard(request):
    if not isinstance(request.user, AdminUser):
        messages.error(request, "You are not authorized to view this page.")
        return redirect('base:login')

    # Get student statistics
    total_students = Student.objects.count()
    approved_students = Student.objects.filter(status='approved').count()
    pending_students = Student.objects.filter(status='pending').count()
    rejected_students = Student.objects.filter(status='rejected').count()  # New count for rejected students

    context = {
        'total_students': total_students,
        'approved_students': approved_students,
        'pending_students': pending_students,
        'rejected_students': rejected_students  # Passing to template
    }

    return render(request, 'pages/admin/dashboard.html', context)

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

@login_required
def approved_students(request):
    students = Student.objects.filter(status='approved')

    # Calculate age from DOB
    today = date.today()
    for student in students:
        if student.dob:
            student.age = today.year - student.dob.year
        else:
            student.age = "N/A"

    return render(request, 'pages/admin/approved_students.html', {'students': students})


@login_required
def rejected_students(request):
    students = Student.objects.filter(status='rejected')

    # Calculate age from DOB
    today = date.today()
    for student in students:
        if student.dob:
            student.age = today.year - student.dob.year
        else:
            student.age = "N/A"

    return render(request, 'pages/admin/rejected_students.html', {'students': students})


