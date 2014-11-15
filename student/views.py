import uuid
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import student_profile, Course
from smvdu_portal.settings import MEDIA_ROOT
from django.core.files.base import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
import os
from django.core import serializers
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.views import password_reset

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context import RequestContext
from .utils import slug2id
from student.form import student_profile_form


# Import the built-in password reset view and password reset confirmation view.
from django.contrib.auth.views import password_reset, password_reset_confirm
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Create your views here.
import datetime

# function that generates random password


def get_password():
    temp_pass = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        pass_exists = User.objects.get(password=temp_pass)
        get_password()
    except:
        return temp_pass




def login_view(request,next='home'):
	if(request.user.is_authenticated()):
		return redirect('home')
		
	if('login' in request.POST):
		username = request.POST.get('username', '')
		password=request.POST.get('password', '')
		user = authenticate(username=username, password=password)
		if(user is not None):
			if user.is_active:
				login(request,user)
				next = request.GET.get('next')
				if next:
					return redirect(next)
				elif user.is_staff:
					return redirect ('/admin')
				else:
				    return redirect('home')
			else:
				return render(request,'login_register.html',{'message_login':"wrong Username or Password"})
		else:
			return render(request,'login_register.html',{'message_login':"wrong Username or Password"})
	if('register' in request.POST):
			#call registration function 
			message=registration_function(request)#store message from registration function 
			return render(request,'login_register.html',{'message_register_alert':message})

	return render(request,'login_register.html',{'message_register_alert':''})

#function for upload the image



def handle_uploaded_file(f, path=''):
    filename = f.name
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()


# function for registration
def registration_function(request):
    R_username = request.POST.get('R_email', '')
    R_fname = request.POST.get('R_fname', '')
    R_lname = request.POST.get('R_lname', '')
    R_email = request.POST.get('R_email', '')
    message_register_alert = ''
    if(R_username == ''):
        message_register_alert = "Enter Username Name"
    elif(R_fname == ''):
        message_register_alert = "Enter First Name"
    elif(R_email == ''):
        message_register_alert = "please Enter the Email ID"
    else:
        try:
            temp_pass = get_password()
            if(User.objects.filter(username=R_username).exists()):
                print "error"
                message_register_alert = "User Already Exits"
            else:
                user = User.objects.create_user(R_username, R_email, temp_pass)
                user.first_name = R_fname
                user.last_name = R_lname
                user.save()
                subject = "Confirmation  mail"
                message = "your password is " + temp_pass
                from_email = settings.EMAIL_HOST_USER
                to_list = [R_username, settings.EMAIL_HOST_USER]
                send_mail(
                    subject, message, from_email, to_list, fail_silently=False)
                message_register_alert = 'success'
        except:
            message_register_alert = "user already exit"
    return message_register_alert


def home(request):
    if 'change_password_submit' in request.POST:
        new_password = request.POST.get('new_password', '')
        if new_password != '':
            request.user.set_password(new_password)
            request.user.save()
            #new_password = make_password(new_password,salt=None,hasher='default')
            # User.objects.select_related().filter(username=request.user.username).update(password=new_password)
            return render(request, 'index.html', {'changed': "password changed successfully"}, context_instance=RequestContext(request))
        else:
            return render(request, 'index.html', context_instance=RequestContext(request))
    return render(request, 'index.html', context_instance=RequestContext(request))


def courses(request):
    return render(request, 'courses.html')


def faculty(request):
	return render(request,'404.html',context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect('home')


def courseView(request):
    if(request.method == 'POST'):
        course_id1 = request.POST.get('course_id', '')
        course_name1 = request.POST.get('course_name', '')
        credits1 = request.POST.get('credits', '')
        end_date1 = request.POST.get('end_date', '')
        start_date1 = request.POST.get('start_date', '')
        image1 = request.FILES.get('image', '')
        image2 = request.FILES.get('image').name
        course_data = course(
            courseid=course_id1,
            coursename=course_name1,
            startdate=start_date1,
            enddate=end_date1,
            image=image2,
            credits=credits1
        )
        course_data.save()

    # else:
    #	form=CourseForm()
    # return render(request,'course.html',{'form':form})
    return render(request, 'course.html', context_instance=RequestContext(request))


def reset(request):
    # Wrap the built-in password reset view and pass it the arguments
    # like the template name, email template name, subject template name
    # and the url to redirect after the password reset is initiated.
    return password_reset(request, template_name='reset.html', post_reset_redirect=reverse('success'))

# This view handles password reset confirmation links. See urls.py file for the mapping.
# This view is not used here because the password reset emails with confirmation links
# cannot be sent from this application.


def reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.

    return password_reset_confirm(request,template_name='reset_confirm.html', uidb64=uidb64, token=token, post_reset_redirect=reverse('success2'))

# This view renders a page with success message.


def success(request):
    return render(request, 'success.html')

def success2(request):
	return render(request,'changed_successfuly.html')

def fc(request):
	return render(request,'fc.html')




def about (request):
	return render(request,'about.html')

@login_required
def all(request):
    """
    Index page for authenticated user
    """
    return render(request, 'notifications/list.html', {
        'notifications': request.user.notifications.all()
    })
    actions = request.user.notifications.all()

    paginator = Paginator(actions, 16) # Show 16 notifications per page
    page = request.GET.get('p')

    try:
        action_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        action_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        action_list = paginator.page(paginator.num_pages)

    return render_to_response('notifications/list.html', {
        'member': request.user,
        'action_list': action_list,
    }, context_instance=RequestContext(request))

@login_required
def unread(request):
    return render(request, 'notifications/list.html', {
        'notifications': request.user.notifications.unread()
    })

@login_required
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)
    return redirect('notifications:all')

@login_required
def mark_as_read(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_read()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')

@login_required
def mark_as_unread(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_unread()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')

@login_required
def delete(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.delete()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')

    
def edit(request):
    if request.method=='POST':
        if student_profile.objects.filter(user_id=request.user.id).exists():
            a=student_profile.objects.get(user_id=request.user.id)
            form = student_profile_form(request.POST, instance=a)
            if form.is_valid():
                j = form.save( commit=False )
                j.save()
            return redirect('home')
        else:
            form=student_profile_form(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user=request.user
                obj.save()
                return redirect('home')
            else:
                return render(request,'edit.html',{'form':form})

    else:
        form=student_profile_form()
        return render(request,'edit.html',{'form':form})

