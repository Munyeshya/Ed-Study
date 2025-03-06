from django.db import models

class Student(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    faculty_of_interest = models.CharField(max_length=255)
    secondary_diploma = models.FileField(upload_to='documents/diplomas/')
    passport = models.FileField(upload_to='documents/passports/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    language_school_letter = models.FileField(upload_to='documents/language_school_letters/', null=True, blank=True)
    responsibility_letter = models.FileField(upload_to='documents/responsibility_letters/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documents for {self.student.full_name}"
