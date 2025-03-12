from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    repeat_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Repeat Password")
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date of Birth")
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=True, label="Gender")

    class Meta:
        model = Student
        fields = ['full_name', 'email', 'contact_info', 'faculty_of_interest', 'dob', 'gender', 'secondary_diploma', 'passport', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
