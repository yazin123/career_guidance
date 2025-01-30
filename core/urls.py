# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('register/', views.register_choice, name='register'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/company/', views.register_company, name='register_company'),
    path('register/college/', views.register_college, name='register_college'),
      path('login/', views.CustomLoginView.as_view(), name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Job URLs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),

    # Application URLs
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/<int:application_id>/update-status/', views.update_application_status, 
         name='update_application_status'),

    # College URLs
    path('college/students/', views.student_list, name='student_list'),
    path('college/students/add/', views.add_student, name='add_student'),
    path('college/students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('college/students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('college/placements/', views.placement_list, name='placement_list'),
    path('college/companies/', views.company_list, name='company_list'),
    path('college/companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('college/companies/invite/', views.invite_company, name='invite_company'),
    path('jobs/<int:job_id>/update-status/', views.update_job_status, name='update_job_status'),

    path('college/placements/export/', views.export_placements, name='export_placements'),
    path('college/students/import/', views.import_students, name='import_students'),

     path('college/students/<int:student_id>/add-placement/', views.add_placement, name='add_placement'),
    

    # Company URLs
    path('company/applicants/', views.company_applicants, name='company_applicants'),
    path('company/jobs/', views.company_jobs, name='company_jobs'),

    # Report URLs
    path('reports/placement/', views.placement_report, name='placement_report'),
    path('reports/company/<int:company_id>/', views.company_report, name='company_report'),      
]

urlpatterns += [
    path('applications/<int:application_id>/update-feedback/', 
         views.update_application_feedback, 
         name='update_application_feedback'),
]