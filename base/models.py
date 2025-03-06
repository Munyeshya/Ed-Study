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

