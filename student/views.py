import uuid
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import student_profile, Course , faculty_profile
from smvdu_portal.settings import MEDIA_ROOT
from django.core.files.base import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
import os
from django.core import serializers
from django.template import RequestContext
from datetime import datetime
from models import Course
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context import RequestContext
from student.form import student_profile_form,faculty_profile_form
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from notification.models import notification

# Import the built-in password reset view and password reset confirmation view.
from django.contrib.auth.views import password_reset, password_reset_confirm
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Create your views here.
import datetime


def handle_uploaded_file(f, path=''):
    filename = f.name
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()


# function for registration


def home(request):
    request.session['last']='home'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'index.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    result_list = notification.objects.filter(receiver=request.user.id,viewed=False)
    print result_list
    request.session['count']= len(result_list)
    print request.session['count']
    return render(request, 'index.html',{'notifications':result_list},context_instance=RequestContext(request))


def courses(request):
    request.session['last']='courses'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'courses.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    return render(request, 'courses.html')


def faculty(request):
    request.session['last']='home'
    return render(request,'faculty.html',context_instance=RequestContext(request))

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

def addmaterial(request):
    return render(request, 'add_material.html')

def admin_courses(request):
    return render(request, 'admin_courses.html')

def admin_course_view(request):
    return render(request, 'admin_course_view.html')

def courseView(request):
    request.session['last']='courses'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'course.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    if(request.method == 'POST'):
        course_id1 = request.POST.get('course_id', '')
        course_name1 = request.POST.get('course_name', '')
        credits1 = request.POST.get('credits', '')
        end_date1 = request.POST.get('end_date', '')
        start_date1 = request.POST.get('start_date', '')
        image1 = request.FILES.get('image', '')
        image2 = request.FILES.get('image').name
        course_data = Course(
            course_id=course_id1,
            course_name=course_name1,
            start_date=start_date1,
            end_date=end_date1,
            image=image2,
            credits=credits1
        )
        course_data.save()
    return render(request, 'course.html', context_instance=RequestContext(request))



def fc(request):
    request.session['last']='courses'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'fc.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    request.session['last']='fc'
    return render(request,'add_question.html')

def dashboard(request):
    request.session['last']='courses'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'fc.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    request.session['last']='fc'
    return render(request,'dashboard.html')


def about (request):
    request.session['last']='courses'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'about.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    request.session['last']='about'
    return render(request,'about.html')



@login_required
def edit(request):
    request.session['last']='courses'
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'edit.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    if request.user.groups.filter(name='student').exists():
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

    else:
        if request.method=='POST':
            if faculty_profile.objects.filter(user_id=request.user.id).exists():
                a=faculty_profile.objects.get(user_id=request.user.id)
                form = faculty_profile_form(request.POST, instance=a)
                if form.is_valid():
                    j = form.save( commit=False )
                    j.save()
                return redirect('home')
            else:
                form=faculty_profile_form(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user=request.user
                    obj.save()
                    return redirect('home')
                else:
                    return render(request,'edit.html',{'form':form})
        else:
            form=faculty_profile_form()
            return render(request,'edit.html',{'form':form})
                                    






@login_required
def mail(request):
    c = Context({'username': settings.EMAIL_HOST_USER })    
    text_content = render_to_string('mail/email.txt', c)
    html_content = render_to_string('mail/fancy-1-2-3.html', c)

    email = EmailMultiAlternatives('Subject', text_content)
    email.attach_alternative(html_content, "text/html")
    email.to = ['vibhanshu86@gmail.com']
    email.send()
    return HttpResponse("SUCCESS")

def changePassword(request):
    if 'change_password_submit' in request.POST:
        new_password = request.POST.get('new_password', '')
        if new_password != '':
            request.user.set_password(new_password)
            request.user.save()
            #new_password = make_password(new_password,salt=None,hasher='default')
            # User.objects.select_related().filter(username=request.user.username).update(password=new_password)
            request.session['changed']=True
    print request.session['last']
    return redirect(request.session['last'])

