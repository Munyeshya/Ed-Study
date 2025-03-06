from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class StudentManager(BaseUserManager):
    def create_user(self, full_name, contact_info, faculty_of_interest, password=None):
        if not full_name or not contact_info or not faculty_of_interest:
            raise ValueError("Students must provide required information")
        
        student = self.model(
            full_name=full_name,
            contact_info=contact_info,
            faculty_of_interest=faculty_of_interest,
        )
        
        if password:
            student.set_password(password)
        else:
            student.set_password(self.make_random_password())  # Set a random password if none provided
        
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, unique=True)
    faculty_of_interest = models.CharField(max_length=255)
    secondary_diploma = models.FileField(upload_to='documents/diplomas/')
    passport = models.FileField(upload_to='documents/passports/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    password = models.CharField(max_length=128, default="")  # Make password field non-nullable

    USERNAME_FIELD = 'contact_info'
    REQUIRED_FIELDS = ['full_name', 'faculty_of_interest']

    objects = StudentManager()

    def __str__(self):
        return self.full_name

class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    language_school_letter = models.FileField(upload_to='documents/language_school_letters/', null=True, blank=True)
    responsibility_letter = models.FileField(upload_to='documents/responsibility_letters/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documents for {self.student.full_name}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.full_name}"

class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.student.full_name}"
 


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class AdminUser(AbstractUser):
    role = models.CharField(max_length=50, default='admin')

    groups = models.ManyToManyField(
        Group,
        related_name="adminuser_groups",  # Avoid conflicts
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="adminuser_permissions",  # Avoid conflicts
        blank=True
    )

    def __str__(self):
        return self.username

