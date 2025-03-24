# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Max, Q
from .models import *
from .forms import *

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
# Add at the top of views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg, Max
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from .models import User, Student, Company, College, Job, Application, Placement
from .forms import (UserForm, StudentForm, CompanyForm, CollegeForm, JobForm, 
                   ApplicationForm, CompanyInviteForm)

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

def home(request):
    jobs = Job.objects.filter(status='OPEN').order_by('-posted_date')[:5]
    context = {
        'jobs': jobs,
    }
    return render(request, 'core/home.html', context)

def register_choice(request):
    return render(request, 'core/register_choice.html')

def register_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'STUDENT'
            user.save()
            
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    
    return render(request, 'core/register_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })

def register_company(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        company_form = CompanyForm(request.POST, request.FILES)
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'COMPANY'
            user.save()
            
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            
            login(request, user)
            messages.success(request, 'Company registration successful!')
            return redirect('dashboard')
    else:
        user_form = UserForm()
        company_form = CompanyForm()
    
    return render(request, 'core/register_company.html', {
        'user_form': user_form,
        'company_form': company_form
    })

def register_college(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        college_form = CollegeForm(request.POST)
        if user_form.is_valid() and college_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'COLLEGE'
            user.save()
            
            college = college_form.save(commit=False)
            college.user = user
            college.save()
            
            login(request, user)
            messages.success(request, 'College registration successful!')
            return redirect('dashboard')
    else:
        user_form = UserForm()
        college_form = CollegeForm()
    
    return render(request, 'core/register_college.html', {
        'user_form': user_form,
        'college_form': college_form
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    context = {}
    
    if request.user.user_type == 'STUDENT':
        context.update({
            'applications': Application.objects.filter(student__user=request.user).order_by('-applied_date')[:5],
            'eligible_jobs': Job.objects.filter(
                status='OPEN',
                min_cgpa__lte=request.user.student.cgpa
            ).order_by('-posted_date')[:5]
        })
    elif request.user.user_type == 'COMPANY':
        context.update({
            'posted_jobs': Job.objects.filter(company__user=request.user).order_by('-posted_date')[:5],
            'recent_applications': Application.objects.filter(
                job__company__user=request.user
            ).order_by('-applied_date')[:5]
        })
    elif request.user.user_type == 'COLLEGE':
        student_count = Student.objects.filter(college__user=request.user).count()
        placed_count = Placement.objects.filter(
            student__college__user=request.user
        ).count()
        
        # Calculate percentage here instead of in template
        placement_percentage = (placed_count / student_count * 100) if student_count > 0 else 0
        
        context.update({
            'student_count': student_count,
            'placed_count': placed_count,
            'placement_percentage': round(placement_percentage, 1),
            'recent_placements': Placement.objects.filter(
                student__college__user=request.user
            ).order_by('-placement_date')[:5]
        })
    
    return render(request, 'core/dashboard.html', context)
# Job Management Views
@login_required
def job_list(request):
    if request.user.user_type == 'COMPANY':
        jobs = Job.objects.filter(company__user=request.user)
    else:
        jobs = Job.objects.all()
    
    # Search and filters
    print("======================")
    
    
    return render(request, 'core/jobs/list.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    can_apply = False
    
    # Calculate application statistics
    total_applications = job.application_set.count()
    shortlisted_count = job.application_set.filter(status='SHORTLISTED').count()
    selected_count = job.application_set.filter(status='SELECTED').count()
    applications = job.application_set.all().order_by('-applied_date')
    
    if request.user.user_type == 'STUDENT':
        student = request.user.student
        can_apply = (
            job.status == 'OPEN' and
            student.cgpa >= job.min_cgpa and
            not Application.objects.filter(student=student, job=job).exists()
        )
    
    context = {
        'job': job,
        'can_apply': can_apply,
        'total_applications': total_applications,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'applications': applications
    }
    return render(request, 'core/jobs/detail.html', context)
@login_required
def create_job(request):
    if request.user.user_type == 'STUDENT'  :
        messages.error(request, 'Only companies or college can post jobs.')
        return redirect('job_list')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            print("=========yes===========")
            if request.user.user_type == 'COMPANY':
                job.company = request.user.company
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_detail', job_id=job.id)
        else:
            print(f"{form.errors}")
    else:
        form = JobForm()
    
    return render(request, 'core/jobs/form.html', {'form': form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company__user=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    
    return render(request, 'core/jobs/form.html', {'form': form, 'job': job})

@login_required
def apply_job(request, job_id):
    if request.user.user_type != 'STUDENT':
        messages.error(request, 'Only students can apply for jobs.')
        return redirect('job_detail', job_id=job_id)
    
    job = get_object_or_404(Job, id=job_id)
    student = request.user.student
    
    # Check if job is open
    if job.status != 'OPEN':
        messages.error(request, 'This job is no longer accepting applications.')
        return redirect('job_detail', job_id=job_id)
    
    # Check if already applied
    if Application.objects.filter(student=student, job=job).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    # Check CGPA requirement
    if student.cgpa < job.min_cgpa:
        messages.error(request, f'Required minimum CGPA is {job.min_cgpa}.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.job = job
            application.status = 'APPLIED'
            application.save()
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('application_list')
    else:
        form = ApplicationForm()
    
    return render(request, 'core/jobs/apply.html', {
        'form': form,
        'job': job,
        'student': student
    })

@login_required
def application_list(request):
    if request.user.user_type == 'STUDENT':
        applications = Application.objects.filter(student__user=request.user)
    elif request.user.user_type == 'COMPANY':
        applications = Application.objects.filter(job__company__user=request.user)
    else:
        applications = Application.objects.filter(
            student__college__user=request.user
        )
    
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    paginator = Paginator(applications.order_by('-applied_date'), 10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    
    return render(request, 'core/applications/list.html', {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES
    })

@login_required
def application_detail(request, application_id):
    if request.user.user_type == 'STUDENT':
        application = get_object_or_404(
            Application, id=application_id, student__user=request.user
        )
    elif request.user.user_type == 'COMPANY':
        application = get_object_or_404(
            Application, id=application_id, job__company__user=request.user
        )
    else:
        application = get_object_or_404(
            Application, id=application_id, student__college__user=request.user
        )
    
    return render(request, 'core/applications/detail.html', {
        'application': application,
        'status_choices': Application.STATUS_CHOICES
    })

@login_required
def update_application_status(request, application_id):
    if request.user.user_type != 'COMPANY':
        messages.error(request, 'Only companies can update application status.')
        return redirect('application_list')
    
    application = get_object_or_404(
        Application, id=application_id, job__company__user=request.user
    )
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated successfully!')
    
    return redirect('application_detail', application_id=application_id)

# College Management Views
@login_required
def student_list(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    students = Student.objects.filter(college__user=request.user)
    
    # Apply filters
    branch = request.GET.get('branch')
    year = request.GET.get('year')
    placement_status = request.GET.get('placement_status')
    
    if branch:
        students = students.filter(branch=branch)
    if year:
        students = students.filter(year_of_passing=year)
    if placement_status:
        if placement_status == 'placed':
            students = students.filter(placement__isnull=False)
        elif placement_status == 'not_placed':
            students = students.filter(placement__isnull=True)
    
    # Get unique values for filters
    branches = Student.objects.filter(college__user=request.user).values_list(
        'branch', flat=True).distinct()
    years = Student.objects.filter(college__user=request.user).values_list(
        'year_of_passing', flat=True).distinct()
    
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    
    context = {
        'students': students,
        'branches': branches,
        'years': years,
    }
    return render(request, 'core/college/students.html', context)

@login_required
def add_student(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'STUDENT'
            user.save()
            
            student = student_form.save(commit=False)
            student.user = user
            student.college = request.user.college
            student.save()
            
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    
    return render(request, 'core/college/student_form.html', {
        'user_form': user_form,
        'student_form': student_form
    })

@login_required
def student_detail(request, student_id):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id, college__user=request.user)
    
    # Calculate application statistics
    total_applications = student.application_set.count()
    shortlisted_applications = student.application_set.filter(status='SHORTLISTED').count()
    selected_applications = student.application_set.filter(status='SELECTED').count()
    
    context = {
        'student': student,
        'total_applications': total_applications,
        'shortlisted_applications': shortlisted_applications,
        'selected_applications': selected_applications,
        'applications': student.application_set.all().order_by('-applied_date'),
        'placements': student.placement_set.all().order_by('-placement_date')
    }
    
    return render(request, 'core/college/student_detail.html', context)

@login_required
def placement_list(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    placements = Placement.objects.filter(student__college__user=request.user)
    
    # Calculate statistics
    total_students = Student.objects.filter(college__user=request.user).count()
    placed_students = placements.values('student').distinct().count()
    placement_percentage = (placed_students / total_students * 100) if total_students > 0 else 0
    
    avg_package = placements.aggregate(Avg('package'))['package__avg'] or 0
    
    # Branch-wise statistics
    branch_stats = []
    branches = Student.objects.filter(college__user=request.user).values_list(
        'branch', flat=True).distinct()
    
    for branch in branches:
        total = Student.objects.filter(
            college__user=request.user, branch=branch).count()
        placed = Placement.objects.filter(
            student__college__user=request.user,
            student__branch=branch
        ).values('student').distinct().count()
        percentage = (placed / total * 100) if total > 0 else 0
        
        branch_stats.append({
            'branch': branch,
            'total': total,
            'placed': placed,
            'percentage': round(percentage, 2)
        })
    
    context = {
        'placements': placements,
        'total_students': total_students,
        'placed_students': placed_students,
        'placement_percentage': round(placement_percentage, 2),
        'avg_package': round(avg_package, 2),
        'branch_stats': branch_stats
    }
    return render(request, 'core/college/placements.html', context)

# Company Management Views
@login_required
def company_list(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    companies = Company.objects.all()
    
    for company in companies:
        company.placement_count = Placement.objects.filter(company=company).count()
        company.active_jobs = Job.objects.filter(
            company=company, status='OPEN').count()
    
    return render(request, 'core/college/companies.html', {'companies': companies})

@login_required
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    context = {
        'company': company,
        'active_jobs': Job.objects.filter(company=company, status='OPEN'),
        'placements': Placement.objects.filter(company=company),
        'total_placements': Placement.objects.filter(company=company).count(),
        'avg_package': Placement.objects.filter(company=company).aggregate(
            Avg('package'))['package__avg'] or 0,
        'highest_package': Placement.objects.filter(company=company).aggregate(
            Max('package'))['package__max'] or 0,
        'total_applications': Application.objects.filter(
            job__company=company).count()
    }
    return render(request, 'core/college/company_detail.html', context)

@login_required
def invite_company(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CompanyInviteForm(request.POST)
        if form.is_valid():
            # Handle invitation email sending logic here
            messages.success(request, 'Invitation sent successfully!')
            return redirect('company_list')
    else:
        form = CompanyInviteForm()
    
    return render(request, 'core/college/invite_company.html', {'form': form})

@login_required
def company_applicants(request):
    if request.user.user_type != 'COMPANY':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    applications = Application.objects.filter(job__company__user=request.user)
    
    # Apply filters
    job_id = request.GET.get('job')
    status = request.GET.get('status')
    
    if job_id:
        applications = applications.filter(job_id=job_id)
    if status:
        applications = applications.filter(status=status)
    
    company_jobs = Job.objects.filter(company__user=request.user)
    
    context = {
        'applications': applications,
        'company_jobs': company_jobs,
        'status_choices': Application.STATUS_CHOICES
    }
    return render(request, 'core/company/applicants.html', context)

@login_required
def company_jobs(request):
    if request.user.user_type != 'COMPANY':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    jobs = Job.objects.filter(company__user=request.user)
    return render(request, 'core/company/jobs.html', {'jobs': jobs})

# Add these to your views.py

@login_required
def delete_job(request, job_id):
    if request.user.user_type != 'COMPANY':
        messages.error(request, 'Only companies can delete jobs.')
        return redirect('job_list')
    
    job = get_object_or_404(Job, id=job_id, company__user=request.user)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('job_list')
        
    return render(request, 'core/jobs/delete.html', {'job': job})

@login_required
def edit_student(request, student_id):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id, college__user=request.user)
    
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        if student_form.is_valid():
            student_form.save()
            messages.success(request, 'Student information updated successfully!')
            return redirect('student_detail', student_id=student.id)
    else:
        student_form = StudentForm(instance=student)
    
    return render(request, 'core/college/student_form.html', {
        'student_form': student_form,
        'student': student
    })
@login_required
def placement_report(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get basic statistics
    total_students = Student.objects.filter(college__user=request.user).count()
    placements = Placement.objects.filter(student__college__user=request.user)
    placed_students = placements.values('student').distinct().count()
    
    # Calculate placement percentage
    placement_percentage = (placed_students / total_students * 100) if total_students > 0 else 0
    
    # Get package statistics
    avg_package = placements.aggregate(Avg('package'))['package__avg'] or 0
    highest_package = placements.aggregate(Max('package'))['package__max'] or 0
    
    # Branch-wise placement statistics
    branch_stats = []
    branches = Student.objects.filter(
        college__user=request.user
    ).values_list('branch', flat=True).distinct()
    
    for branch in branches:
        branch_total = Student.objects.filter(
            college__user=request.user, 
            branch=branch
        ).count()
        
        branch_placed = Placement.objects.filter(
            student__college__user=request.user,
            student__branch=branch
        ).values('student').distinct().count()
        
        branch_percentage = (branch_placed / branch_total * 100) if branch_total > 0 else 0
        
        branch_avg_package = Placement.objects.filter(
            student__college__user=request.user,
            student__branch=branch
        ).aggregate(Avg('package'))['package__avg'] or 0
        
        branch_stats.append({
            'branch': branch,
            'total_students': branch_total,
            'placed_students': branch_placed,
            'placement_percentage': round(branch_percentage, 2),
            'average_package': round(branch_avg_package, 2)
        })
    
    # Company-wise placement statistics
    company_stats = Placement.objects.filter(
        student__college__user=request.user
    ).values('company__name').annotate(
        student_count=Count('student', distinct=True),
        avg_package=Avg('package'),
        max_package=Max('package')
    )
    
    # Year-wise placement statistics
    year_stats = Placement.objects.filter(
        student__college__user=request.user
    ).values('student__year_of_passing').annotate(
        total_placements=Count('id'),
        avg_package=Avg('package')
    ).order_by('-student__year_of_passing')
    
    context = {
        'total_students': total_students,
        'placed_students': placed_students,
        'placement_percentage': round(placement_percentage, 2),
        'avg_package': round(avg_package, 2),
        'highest_package': highest_package,
        'branch_stats': branch_stats,
        'company_stats': company_stats,
        'year_stats': year_stats,
        
        # Additional Statistics
        'multiple_offers': Student.objects.filter(
            college__user=request.user,
            placement__isnull=False
        ).annotate(
            offer_count=Count('placement')
        ).filter(offer_count__gt=1).count(),
        
        'pending_applications': Application.objects.filter(
            student__college__user=request.user,
            status='PENDING'
        ).count()
    }
    
    return render(request, 'core/reports/placement_report.html', context)

@login_required
def company_report(request, company_id):
    if request.user.user_type not in ['COLLEGE', 'COMPANY']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    company = get_object_or_404(Company, id=company_id)
    
    # Basic Statistics
    total_jobs = Job.objects.filter(company=company).count()
    total_applications = Application.objects.filter(job__company=company).count()
    total_selections = Application.objects.filter(
        job__company=company, 
        status='SELECTED'
    ).count()
    
    # Job Statistics
    job_stats = Job.objects.filter(company=company).annotate(
        application_count=Count('application'),
        selected_count=Count('application', filter=Q(application__status='SELECTED')),
        shortlist_rate=Count('application', filter=Q(application__status='SHORTLISTED')) * 100.0 / Count('application'),
        selection_rate=Count('application', filter=Q(application__status='SELECTED')) * 100.0 / Count('application')
    )
    
    # College-wise Statistics
    college_stats = Application.objects.filter(
        job__company=company
    ).values(
        'student__college__name'
    ).annotate(
        total_applications=Count('id'),
        selected_students=Count('id', filter=Q(status='SELECTED')),
        selection_rate=Count('id', filter=Q(status='SELECTED')) * 100.0 / Count('id')
    )
    
    # Placement Statistics
    placements = Placement.objects.filter(company=company)
    avg_package = placements.aggregate(Avg('package'))['package__avg'] or 0
    highest_package = placements.aggregate(Max('package'))['package__max'] or 0
    
    # Branch-wise placement statistics
    branch_placements = Placement.objects.filter(
        company=company
    ).values('student__branch').annotate(
        count=Count('id'),
        avg_package=Avg('package')
    )
    
    context = {
        'company': company,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_selections': total_selections,
        'selection_rate': (total_selections / total_applications * 100) if total_applications > 0 else 0,
        
        # Job Related Statistics
        'job_stats': job_stats,
        'active_jobs': Job.objects.filter(company=company, status='OPEN').count(),
        
        # Application Statistics
        'pending_applications': Application.objects.filter(
            job__company=company, 
            status='PENDING'
        ).count(),
        'shortlisted_applications': Application.objects.filter(
            job__company=company, 
            status='SHORTLISTED'
        ).count(),
        
        # Placement Statistics
        'placements': placements,
        'placed_students_count': placements.count(),
        'avg_package': round(avg_package, 2),
        'highest_package': highest_package,
        'branch_placements': branch_placements,
        'college_stats': college_stats,
        
        # Timeline
        'recent_applications': Application.objects.filter(
            job__company=company
        ).order_by('-applied_date')[:10],
        'recent_placements': placements.order_by('-placement_date')[:10]
    }
    
    return render(request, 'core/reports/company_report.html', context)
        

import csv
from django.core.exceptions import ValidationError

@login_required
def import_students(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('import_students')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            success_count = 0
            error_count = 0
            
            for row in reader:
                try:
                    # Create user
                    user = User.objects.create_user(
                        username=row['Email'],  # Using email as username
                        email=row['Email'],
                        password='temp123',  # Temporary password
                        first_name=row['First Name'],
                        last_name=row['Last Name'],
                        user_type='STUDENT'
                    )
                    
                    # Create student
                    Student.objects.create(
                        user=user,
                        college=request.user.college,
                        roll_number=row['Roll Number'],
                        branch=row['Branch'],
                        year_of_passing=int(row['Year of Passing']),
                        cgpa=float(row['CGPA'])
                    )
                    
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            if success_count:
                messages.success(request, f'Successfully imported {success_count} students.')
            if error_count:
                messages.warning(request, f'Failed to import {error_count} students.')
                
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            
    return render(request, 'core/college/import_students.html')


from django.http import HttpResponse
import csv

@login_required
def export_placements(request):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="placements.csv"'

    # Create the CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow([
        'Student Name', 
        'Roll Number',
        'Branch',
        'CGPA',
        'Company',
        'Position',
        'Package (LPA)',
        'Location',
        'Placement Date'
    ])

    # Get all placements for the college
    placements = Placement.objects.filter(
        student__college__user=request.user
    ).select_related('student', 'student__user', 'company')

    # Write the data rows
    for placement in placements:
        writer.writerow([
            placement.student.user.get_full_name(),
            placement.student.roll_number,
            placement.student.branch,
            placement.student.cgpa,
            placement.company.name,
            placement.designation,
            placement.package,
            placement.location,
            placement.placement_date.strftime('%Y-%m-%d')
        ])

    return response

@login_required
def add_placement(request, student_id):
    if request.user.user_type != 'COLLEGE':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id, college__user=request.user)
    
    if request.method == 'POST':
        form = PlacementForm(request.POST)
        if form.is_valid():
            placement = form.save(commit=False)
            placement.student = student
            placement.save()
            messages.success(request, 'Placement record added successfully!')
            return redirect('student_detail', student_id=student.id)
    else:
        # Get relevant job if student has any accepted applications
        initial_data = {}
        selected_application = Application.objects.filter(
            student=student, 
            status='SELECTED'
        ).first()
        
        if selected_application:
            initial_data = {
                'company': selected_application.job.company,
                'job': selected_application.job,
                'designation': selected_application.job.title
            }
        form = PlacementForm(initial=initial_data)
    
    context = {
        'form': form,
        'student': student
    }
    return render(request, 'core/college/add_placement.html', context)

@login_required
def update_job_status(request, job_id):
    if request.user.user_type != 'COMPANY':
        messages.error(request, 'Only companies can update job status.')
        return redirect('job_detail', job_id=job_id)
    
    job = get_object_or_404(Job, id=job_id, company__user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Job.STATUS_CHOICES):
            job.status = new_status
            job.save()
            messages.success(request, f'Job status updated to {job.get_status_display()}.')
    
    return redirect('job_detail', job_id=job_id)


@login_required
def update_application_feedback(request, application_id):
    if request.user.user_type != 'COMPANY':
        messages.error(request, 'Only companies can provide feedback.')
        return redirect('application_detail', application_id=application_id)
    
    application = get_object_or_404(
        Application, 
        id=application_id, 
        job__company__user=request.user
    )
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        application.feedback = feedback
        application.save()
        messages.success(request, 'Feedback updated successfully.')
    
    return redirect('application_detail', application_id=application_id)