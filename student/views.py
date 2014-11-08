import uuid
from django.db.models import Q
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import user,student
from smvdu_portal.settings import MEDIA_ROOT
from django.core.files.base import File
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_password():
	temp_pass=str(uuid.uuid4())[:11].replace('-','')
	try:
		pass_exists=user.objects.get(password=temp_pass)
		get_password()
	except:
		return temp_pass
# Create your views here.
import datetime

#function that generates random password
def get_password():
    temp_pass = str(uuid.uuid4())[:11].replace('-','').lower()
    try:
        pass_exists = user.objects.get(password=temp_pass)
        get_password()
    except:
        return temp_pass
    
    
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
		username = request.POST.get('username', '')
		password=request.POST.get('password', '')
		if(username!='' and password!=''):
			try:
				result=user.objects.filter(username=username).values()[0]
				if(result['password']==password):
					return render(request,'login_register.html')
				else:
					return render(request,'login_register.html',{'message_login':"wrong Username or Password"})
			except:
				return render(request,'login_register.html',{'message_login':"wrong Username or Password"})

	if('register' in request.POST):
		#call registration function 
		message=registration_function(request)#store message from registration function 
		return render(request,'login_register.html',{'message_register_alert':message})

	return render(request,'login_register.html',{'message_register_alert':''})

#function for course
def courses(request):
	return render_to_response('courses.html')
	

#function for faculty
def faculty(request):
	return render_to_response('faculty.html')



#function for upload the image
def handle_uploaded_file(f,path=''):
    filename = f.name
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()




#function for registration
def registration_function(request):
		R_username = request.POST.get('R_username', '')
		R_fname=request.POST.get('R_fname','')
		R_lname=request.POST.get('R_lname')
		_file = request.FILES.get('R_Image','')
		message_register_ale=''
		if(R_username==''):
			message_register_alert="Enter Username Name"
		elif(R_fname==''):
			message_register_alert="Enter First Name"
		elif(_file==''):
			message_register_alert="please uplaod the image file"
		else:
			try:
				user_exists = user.objects.get(username=R_username)
				message_register_alert="User with this email is already registered"
			except:
				temp_pass = get_password()
				filename=request.FILES.get('R_Image').name
				handle_uploaded_file(request.FILES.get('R_Image'))
				user_table = user(username=R_username,password=temp_pass,status=True)
				user_table.save()

				subject="Confirmation  mail"
				message = "your password is " + temp_pass
				from_email = settings.EMAIL_HOST_USER
				to_list=[R_username,settings.EMAIL_HOST_USER]
				send_mail(subject,message,from_email,to_list, fail_silently=False)
				message_register_alert='your password has been sent to your email'
		return message_register_alert
