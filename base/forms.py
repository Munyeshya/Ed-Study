from django import forms
from .models import Student, Faculty

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    repeat_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Repeat Password")
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date of Birth")
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=True, label="Gender")
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True, label="Faculty of Choice")  # Dropdown for Faculty

    class Meta:
        model = Student
        fields = ['full_name', 'email', 'contact_info', 'faculty', 'dob', 'gender', 'secondary_diploma', 'passport', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
