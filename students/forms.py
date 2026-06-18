from django import forms
from .models import Student

class ContactForm(forms.Form):
    name    = forms.CharField(max_length=50, label="Your Name")
    email   = forms.EmailField(label="Your Email")
    age     = forms.IntegerField(min_value=16, max_value=60, required=False, label="Age")
    message = forms.CharField(widget=forms.Textarea, label="Message")

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll', 'name', 'email', 'marks', 'department', 'image', 'resume', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@college.edu'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'roll': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@college.edu'):
            raise forms.ValidationError("Use your official @college.edu email.")
        return email

    def clean(self):
        cleaned = super().clean()
        marks = cleaned.get('marks')
        dept = cleaned.get('department')
        if marks is not None and dept and dept.name == 'CSE' and marks < 40:
            raise forms.ValidationError("CSE requires minimum 40 marks.")
        return cleaned
