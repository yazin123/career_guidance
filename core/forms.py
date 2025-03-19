# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Company, College, Job, Application, Placement

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user', 'college')
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'credentials': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ( 'status', 'posted_date')
        widgets = {
             'company': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'eligible_branches': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your cover letter here...'
            })
        }

# core/forms.py
class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placement
        fields = ['company', 'job', 'designation', 'package', 'location', 'placement_date']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'job': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'package': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'placement_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job'].required = False  # Make job field optional

class CompanyInviteForm(forms.Form):
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))


    