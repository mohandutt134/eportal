from django.shortcuts import render
from django.conf import settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
def quiz(request):
	return render(request,'course.html')

def edit_spec(request):
    return render(request, 'edit_spec.html')

def quiz_control(request):
    return render(request, 'quiz_control.html')

def add_question(request):
    return render(request, 'add_question.html')

def attach_question(request):
    return render(request, 'attach_question.html')

def quiz_confirm(request):
    return render(request, 'quiz_confirm.html')