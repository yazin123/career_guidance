from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('COLLEGE', 'College'),
        ('COMPANY', 'Company'),
        ('STUDENT', 'Student')
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

class College(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    description = models.TextField()
    credentials = models.FileField(upload_to='company_credentials/', blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    branch = models.CharField(max_length=100)
    year_of_passing = models.IntegerField()
    cgpa = models.FloatField()
    resume = models.FileField(upload_to='student_resumes/', blank=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.roll_number}"

class Job(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)  # Full-time, Part-time, Internship
    salary_range = models.CharField(max_length=100)
    deadline = models.DateField()
    posted_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    min_cgpa = models.FloatField(default=0)
    eligible_branches = models.CharField(max_length=500)  # Comma-separated list

    def __str__(self):
        return f"{self.title} at {self.company.name}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('REVIEWING', 'Under Review'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEWED', 'Interviewed'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    cover_letter = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('student', 'job')

class Placement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)  # Make job optional
    designation = models.CharField(max_length=100)
    package = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    placement_date = models.DateField()