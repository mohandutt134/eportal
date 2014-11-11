import uuid
from django.db.models import Q
from django.shortcuts import render_to_response,HttpResponseRedirect,render,redirect
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import user,student
from smvdu_portal.settings import MEDIA_ROOT
from django.core.files.base import File
from django.contrib.auth.hashers import check_password,make_password                                                                                                       
import os
from django.core import serializers
from django.template import RequestContext
BASE_DIR = os.path.dirname(os.path.dirname(__file__))




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
    
    


def login(request):
	if 'uname' in request.session:
		return redirect('home')
	else:
		if('login' in request.POST):
			username = request.POST.get('username', '')
			password=request.POST.get('password', '')
			if(username!='' and password!=''):
				try:
					result=user.objects.filter(username=username).values()[0]

					if(check_password(password, result['password'])):
						request.session['uname'] = username
						try:
							info = student.objects.get(username=request.session['uname'])
							status="student"
						except:
							info = student.objects.get(username=request.session['uname'])
							status="faculty"
						request.session['info_dic']={
							'fname': info.FirstName,
							'lname': info.LastName,
							'status':status
						}
						return redirect('home')
						#return render(request,'login_register.html',{'message_login':request.session['uname']})
					else:
						return render(request,'login_register.html',{'message_login':"wrong Username or Password"})
				except:
					return render(request,'login_register.html',{'message_login':"wrong Username or Password"})

		if('register' in request.POST):
			#call registration function 
			message=registration_function(request)#store message from registration function 
			return render(request,'login_register.html',{'message_register_alert':message})

		return render(request,'login_register.html',{'message_register_alert':''})

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
		R_lname=request.POST.get('R_lname','')
		R_date=request.POST.get('R_date')
		_file = request.FILES.get('R_Image','')
		message_register_alert=''
		if(R_username==''):
			message_register_alert="Enter Username Name"
		elif(R_fname==''):
			message_register_alert="Enter First Name"
		elif(_file==''):
			message_register_alert="please uplaod the image file"
		else:
			try:
				user_exists = user.objects.get(username=R_username)
				message_register_alert="You are already registered"
			except:
				temp_pass = get_password()
				temp_hashed_pass = make_password(temp_pass, salt=None, hasher='default')
				filename=request.FILES.get('R_Image').name
				handle_uploaded_file(request.FILES.get('R_Image'))
				user_table = user(username=R_username,password=temp_hashed_pass,status=True)
				
				#date store in the student table
				student_table=student(username=R_username,FirstName=R_fname,LastName=R_lname,DOB=R_date,Semester='',Branch='',image=filename)
				student_table.save()
				user_table.save()
				subject="Confirmation  mail"
				message = "your password is " + temp_pass
				from_email = settings.EMAIL_HOST_USER
				to_list=[R_username,settings.EMAIL_HOST_USER]

				send_mail(subject,message,from_email,to_list, fail_silently=False)
				message_register_alert='success'
		return message_register_alert

			

def home(request):
	if 'change_password_submit' in request.POST:
		new_password=request.POST.get('new_password', '')
		if new_password!='':
			new_password = make_password(new_password,salt=None,hasher='default')
			user.objects.select_related().filter(username=request.session['uname']).update(password=new_password)
			return render(request,'index.html',{'changed':"password changed successfully"},context_instance=RequestContext(request))
		else:
			return render(request,'index.html',context_instance=RequestContext(request))
	return render_to_response('index.html',context_instance=RequestContext(request))
	
def courses(request):
	return render(request,'courses.html')
def faculty(request):
	return render(request,'courses.html',context_instance=RequestContext(request))
def logout(request):
	if 'uname' in request.session:
		del request.session['uname']
		del request.session['info_dic']
	return redirect('home')


