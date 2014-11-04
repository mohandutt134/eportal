from django.db.models import Q
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.context_processors import csrf
from student.models import user

# Create your views here.
from django.shortcuts import render_to_response
import datetime
def home(request):
	username = request.POST.get('username', '')
	password=request.POST.get('password', '')
	if(username!='' and password!=''):
		b = user(username=username,password=password)
		b.save()
	else:
		now = datetime.datetime.now()
	now = datetime.datetime.now()
	return render(request,'index.html', {'current_date': now})

def login(request):
	username = request.POST.get('username', '')
	password=request.POST.get('password', '')
	if(username!='' and password!=''):
		b = user(username=username,password=password)
		b.save()
	return render(request,'login_register.html',{})