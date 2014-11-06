from django.db.models import Q
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.context_processors import csrf
from student.models import user

# Create your views here.
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
	
	
	if('login' in request.POST):
		ausername = request.POST.get('username', '')
		password=request.POST.get('password', '')
		if(ausername!='' and password!=''):
			result=user.objects.filter(username=ausername).values()[0]
			if(result['password']==password):
				return render(request,'login_register.html',{'message':result['password']})
			else:
				return render(request,'login_register.html',{'message':"wrong password"})

	if('register' in request.POST):
		R_username=request.POST.get('R_username','')
		R_password=request.POST.get('R_password','')
		if(R_username!='' and R_password!=''):
			b = user(username=R_username,password=R_password)
			b.save()
	return render(request,'login_register.html',{'message':""})