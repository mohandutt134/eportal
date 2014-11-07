import uuid
from django.db.models import Q
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import user

def get_password():
	temp_pass=str(uuid.uuid4())[:11].replace('-','')
	try:
		pass_exists=user.objects.get(password=temp_pass)
		get_password()
	except:
		return temp_pass
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
		if(R_username!=''):
			temp_pass=get_password()
			b = user(username=R_username,password=temp_pass)
			b.save()
			subject="Com"
			message="password" + temp_pass
			from_email = settings.EMAIL_HOST_USER
			to_list = [R_username,settings.EMAIL_HOST_USER]
			send_mail(subject,message,from_email,to_list,fail_silently=False)
	return render(request,'login_register.html',{'message':""})