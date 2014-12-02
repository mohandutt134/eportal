import uuid
from django import template
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import student_profile, Course , faculty_profile,material
from attendance.models import attendance
from smvdu_portal.settings import MEDIA_ROOT
from django.core.files.base import File
from django.contrib.auth.models import User
from django.contrib.auth import models
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
from student.form import student_profile_form,faculty_profile_form,add_material_form,update_faculty_image,update_student_image
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from notification.models import notification,activity
from django.core.exceptions import PermissionDenied
from quiz.models import *


# Import the built-in password reset view and password reset confirmation view.
from django.contrib.auth.views import password_reset, password_reset_confirm
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Create your views here.
import datetime


def handle_uploaded_file(f,uname, path):
    f.name= uname+".jpg"
    print uname
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(f.name)), 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()


# function for registration


def home(request):
    request.session['last']='home'
    if request.user.is_authenticated():
        return redirect('dashboard')
    if 'changed' in request.session:
        del request.session['changed']
        return render(request, 'index.html',{'changed': "password changed successfully"}, context_instance=RequestContext(request))
    result_list = notification.objects.filter(receiver=request.user.id,viewed=False)
    print result_list
    request.session['count']= len(result_list)
    print request.session['count']
    return render(request, 'index.html',{'notifications':result_list},context_instance=RequestContext(request))



def test(request):
    return render (request,'student_course.html')
    # try:
    #     if request.user.is_authenticated():
    #         if request.user.groups.filter(name='faculty').exists():
    #             return render(request,'courseinfo.html',{'temp':'base/sidebarf.html','usr':request.user})
    #         else:
    #             return render(request,'courseinfo.html',{'temp':'base/sidebars.html','usr':request.user})
    #     else:
    #         return render(request,'courseinfo.html',{'temp':'base/header.html','usr':request.user})
    # except Exception, e:
    #     return HttpResponse(e)


def edit_spec(request):
    return render(request, 'edit_spec.html')

def quiz_control(request):
    return render(request, 'quiz_control.html')

def add_question(request):
    return render(request, 'add_question.html')

def attach_question(request):
    return render(request, 'attach_question.html')

def quiz_confirm(request):
    return render(request, 'public_courses.html')


@login_required
def add_material(request,id=None):
    if request.session['type']=='faculty':
        try:
            course = Course.objects.get(course_id=id)
            if course.facultyassociated==request.user.faculty_profile:
                if request.method=='POST':
                    if 'save' in request.POST:
                        form=add_material_form(request.POST,request.FILES)
                        print form
                        if form.is_valid():
                            j=form.save(commit=False)
                            course=Course.objects.get(course_id=id)
                            j.course=course
                            j.addedby=request.user
                            j.save()
                            subject="New Material Added: "+j.title
                            activity.objects.create(subject=subject,course=course)
                            students = student_profile.objects.filter(coursetaken=course)
                            link = '/course/'+id
                            for student in students:
                                notification.objects.create(title="Course Update",body="New Material has been added",link=link,course=course,receiver=student.user,sender=request.user)
                            return redirect('course',id=id)
                        else:
                            print form.errors
                            return render(request,'add_material.html',{'form':form})
                else:
                    form=add_material_form()
                    return render(request,'add_material.html',{'form':form})
            else:
                raise PermissionDenied
        except Exception as e:
            return HttpResponse(e)

def pprofile (request,username=None):
    try:
        usr =  User.objects.get(username=username)        
        if request.user.is_authenticated():
            if request.user.groups.filter(name='faculty').exists():
                return render(request,'pprofile.html',{'temp':'base/sidebarf.html','usr':usr})
            else:
                return render(request,'pprofile.html',{'temp':'base/sidebars.html','usr':usr})
        else:
            return render(request,'pprofile.html',{'temp':'base/header.html','usr':usr})
    except Exception, e:
        return HttpResponse(e)

@login_required
def courses(request):
    if request.session['type'] == 'faculty':
        try:
            faculty=faculty_profile.objects.get(user=request.user)
            courses = Course.objects.filter(facultyassociated=faculty)
        except:
            courses=None
        return render(request, 'courses.html',{'temp':'base/sidebarf.html','courses':courses})

    else:
        return redirect('dashboard')


@login_required
def course(request,id=None):
    if request.session['type'] == 'faculty':
        try:
            course = Course.objects.get(course_id=id)
            if course.facultyassociated==request.user.faculty_profile:
                activities = activity.objects.filter(course=course)
                return render(request, 'admin_course_view.html',{'course':course,'activities':activities})
            else:
                raise PermissionDenied()
                
        except Exception as e:
            return HttpResponse(e)
        return render(request, 'admin_course_view.html',{'course':course})
    else:
        try:
            course = Course.objects.get(course_id=id)
            if course in request.user.student_profile.coursetaken.all():
                activities = activity.objects.filter(course=course)
                materials = material.objects.filter(course=course)
                total = attendance.objects.filter(course=course).count()
                quiz=quiz_spec.objects.filter(course=course)
                total_p = attendance.objects.filter(course=course,present=request.user.student_profile).count()
                #Filter quizes and render them
                #Filter announcements
                #Filter assignmen
                return render(request, 'student_course.html',{'course':course,'activities':activities,'materials':materials,'total':total,'total_p':total_p,'quizes':quiz})
            else:
                raise PermissionDenied()
        except Exception as e:
            return HttpResponse(e)





def allcourses(request):
    temp='base/header.html'
    if 'type' in request.session:
        if request.session['type']=='faculty':
            temp='base/sidebarf.html'
        else:
            temp='base/sidebars.html'

    if request.method =='POST':
        if 'search' in request.POST:
            string = request.POST.get('search_string')
            courses = Course.objects.filter(course_name__icontains=string)
            return render(request, 'public_courses.html',{'temp':temp,'courses':courses})

        elif 'category' in request.POST:
            dept = request.POST.get('department')
            sem = request.POST.get('semester')
            if sem == 'all':
                courses = Course.objects.filter(dept=dept)
            else:
                courses = Course.objects.filter(dept=dept,semester=sem)
            return render(request, 'public_courses.html',{'temp':temp,'courses':courses})
        else:
            raise PermissionDenied
    else:
        courses = Course.objects.filter(dept='CSE')
        return render(request, 'public_courses.html',{'temp':temp,'courses':courses})




@login_required
def dashboard(request):
    faculty_cse = faculty_profile.objects.filter(department="CSE")
    faculty_ece = faculty_profile.objects.filter(department="ECE")
    faculty_mec = faculty_profile.objects.filter(department="MEC")
    faculty_ibt = faculty_profile.objects.filter(department="IBT")
    if request.user.groups.filter(name='faculty').exists():
        request.session['type']='faculty'
        courses = Course.objects.filter(facultyassociated=request.user.faculty_profile)
        return render(request, 'dashboard.html',{'temp':'base/sidebarf.html','courses':courses,'faculty_cse':faculty_cse,'faculty_ece':faculty_ece,'faculty_mec':faculty_mec,'faculty_ibt':faculty_ibt},context_instance=RequestContext(request))

    else:
        request.session['type']='student'
        courses = request.user.student_profile.coursetaken.all()
        return render(request,'dashboard.html',{'temp':'base/sidebars.html','courses':courses,'faculty_cse':faculty_cse,'faculty_ece':faculty_ece,'faculty_mec':faculty_mec,'faculty_ibt':faculty_ibt})



def about (request):
    return render(request,'template.html')


@login_required
def profile_edit(request):
    uname = request.POST.get('username','')
    fname = request.POST.get('first_name','')
    lname = request.POST.get('last_name','')
    dept = request.POST.get('department','')
    rsrch = request.POST.get('research','')
    aoi = request.POST.get('aoi','')
    des = request.POST.get('description','')
    web = request.POST.get('weburl','')
    User.objects.filter(username=uname).update(first_name=fname,last_name=lname)

    faculty_profile.objects.filter(user= User.objects.get(username=uname)).update(department=dept,description=des,research=rsrch,areaofinterest=aoi,weburl=web)
    return redirect('/profile')

@login_required
def profile_edit_student(request):
    uname = request.POST.get('username','')
    fname = request.POST.get('first_name','')
    lname = request.POST.get('last_name','')
    dept = request.POST.get('department','')
    rsrch = request.POST.get('research','')
    aoi = request.POST.get('aoi','')
    des = request.POST.get('description','')
    web = request.POST.get('weburl','')
    User.objects.filter(username=uname).update(first_name=fname,last_name=lname)

    faculty_profile.objects.filter(user= User.objects.get(username=uname)).update(department=dept,description=des,research=rsrch,areaofinterest=aoi,weburl=web)
    return redirect('/profile')


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
    redirect_to = request.GET.get('next','')
    if 'change_password_submit' in request.POST:
        new_password = request.POST.get('new_password', '')
        if new_password != '':
            request.user.set_password(new_password)
            request.user.save()
            notification.objects.create(title="Confirmation",body="Password Changed Successfully",link="#",receiver=request.user,sender=request.user)
    return redirect(redirect_to)

@login_required
def profile (request):

    if request.method=='POST':
        uname = request.POST.get('username','')
        fname = request.POST.get('first_name','')
        lname = request.POST.get('last_name','')
        User.objects.filter(username=uname).update(first_name=fname,last_name=lname)
        if 'department' in request.POST:
            dept = request.POST.get('department','')
            rsrch = request.POST.get('research','')
            aoi = request.POST.get('aoi','')
            des = request.POST.get('description','')
            web = request.POST.get('weburl','')
            image=request.FILES.get('image','')
            if image:
                handle_uploaded_file(image,request.user.username,'fpp/')
            #print image.name
            else:
                image = request.user.faculty_profile.image
            print image
            faculty_profile.objects.filter(user= User.objects.get(username=uname)).update(department=dept,description=des,research=rsrch,areaofinterest=aoi,weburl=web,image=image)
            #return render(request,'profile.html',{'temp':'base/sidebarf.html','msg':"Profile has been successfully updated"})
            return redirect('profile')
        else:
            brnch = request.POST.get('branch','')
            sem = request.POST.get('sem','')
            dob = request.POST.get('dateofbirth','')
            image=request.FILES.get('dp','')
            if image:
                handle_uploaded_file(image,request.user.username,'spp/')
            #print image.name
            else:
                image = request.user.student_profile.image
            print image
            student_profile.objects.filter(user= User.objects.get(username=uname)).update(Branch=brnch,Semester=sem,DOB=dob,image=image)
            return redirect('profile')
            #return render(request,'student_profile.html',{'temp':'base/sidebars.html','msg':"Profile has been successfully updated"})
    else:
        if request.user.groups.filter(name='faculty').exists():
            form=update_faculty_image()
            return render(request,'profile.html',{'temp':'base/sidebarf.html','form':form})
        else:
            form=update_student_image()
            return render(request,'student_profile.html',{'temp':'base/sidebars.html','form':form})

def course_info(request,id):
    try:
        course = Course.objects.get(course_id=id)
        if 'type' in request.session:
            if request.session['type']=='student':
                count = student_profile.objects.filter(user=request.user,coursetaken=course).count()
                return render(request,'courseinfo.html',{'temp':'base/sidebars.html','course':course,'count':count})
            else:
                return render(request,'course_info.html',{'temp':'base/sidebarf.html','course':course,'faculty':"isfaculty"})
        return render(request,'courseinfo.html',{'temp':'base/header.html','course':course})
    except Exception as e:
        return HttpResponse(e)
def faculties(request):
    temp='base/header.html'
    if 'type' in request.session:
        if request.session['type']=='faculty':
            temp='base/sidebarf.html'
        else:
            temp='base/sidebars.html'

    if request.method =='POST':
        if 'category' in request.POST:
            dept = request.POST.get('department')
            faculties = faculty_profile.objects.filter(department=dept)
            return render(request, 'faculty_list.html',{'temp':temp,'faculties':faculties})
        else:
            raise PermissionDenied
    else:
        faculties = faculty_profile.objects.filter(department='CSE')
        return render(request, 'faculty_list.html',{'temp':temp,'faculties':faculties})

