from django.contrib import admin
from .models import Student, Document, Payment, Notification, AdminUser,Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name']  # Display faculty names in admin panel

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'contact_info', 'faculty', 'status', 'created_at')  # Changed faculty_of_interest → faculty
    list_filter = ('status', 'faculty')  # Changed faculty_of_interest → faculty
    search_fields = ('full_name', 'email', 'contact_info')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'language_school_letter', 'responsibility_letter', 'uploaded_at')
    search_fields = ('student__full_name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__full_name', 'transaction_id')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('student__full_name',)

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
