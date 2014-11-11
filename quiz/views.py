from django.shortcuts import render
from django.conf import settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
def quiz(request):
	if 'uname' in request.session:
		return render(request,'courses.html',{'logged':request.session['info_dic']})
	return render(request,'courses.html')
