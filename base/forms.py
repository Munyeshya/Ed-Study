from django import forms
from .models import Student, AdminUser

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['full_name', 'email', 'faculty_of_interest', 'secondary_diploma', 'passport', 'password']

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = AdminUser
        fields = ['email', 'password']

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.set_password(self.cleaned_data['password'])
        if commit:
            admin.save()
        return admin
