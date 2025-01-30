# core/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def college_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'COLLEGE':
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Access denied. College privileges required.')
            return redirect('dashboard')
    return wrap

def company_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'COMPANY':
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Access denied. Company privileges required.')
            return redirect('dashboard')
    return wrap

def student_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'STUDENT':
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Access denied. Student privileges required.')
            return redirect('dashboard')
    return wrap