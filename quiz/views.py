from django.shortcuts import render
from django.conf import settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
def quiz(request):
	return render(request,'courses.html')
