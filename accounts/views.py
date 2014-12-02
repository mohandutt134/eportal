from django.shortcuts import render
import uuid
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
import os
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.views import password_reset,password_reset_confirm
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.contrib.auth.models import Group
from notification.models import notification
from student.models import Course,faculty_profile,student_profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


def login_view(request,next='home'):
    if(request.user.is_authenticated()):
        return redirect('home')
        
    if('login' in request.POST):
        username = request.POST.get('username', '')
        password=request.POST.get('password', '')
        print username+password
        user = authenticate(username=username, password=password)
        print user
        if(user is not None):
            if user.is_active:
                login(request,user)
                next = request.GET.get('next')
                print "admin"
                if next:
                    return redirect(next)
                elif user.is_staff:
                    return redirect ('/admin') 
                else:
                    return redirect('home')
            else:
                return render(request,'accounts/login.html',{'message_login':"Your account is inactive"})
        else:
            return render(request,'accounts/login.html',{'message_login':"wrong Username or Password"})
    if('register' in request.POST):
            #call registration function 
            message=registration_function(request)#store message from registration function 
            return render(request,'accounts/login.html',{'message_register_alert':message})

    return render(request,'accounts/login.html',{'message_register_alert':''})

def logout_view(request):
    logout(request)
    return redirect('home')


def register2(request):
    if(request.user.is_authenticated()):
        return redirect('home')
    if request.method=="POST":
        print "inside"
        msg=registration_function(request)
        return render (request,'accounts/register.html',{"msg":msg})
    else:
        return render (request,'accounts/register.html')

def registration_function(request):
    R_username = request.POST.get('R_email', '')
    R_fname = request.POST.get('R_fname', '')
    R_lname = request.POST.get('R_lname', '')
    R_email = request.POST.get('R_email', '')
    R_email = R_email + "@smvdu.ac.in"
    R_category=request.POST.get('category','')
    message_register_alert = ''
    if(R_username == ''):
        message_register_alert = "Enter Username Name"
    elif(R_fname == ''):
        message_register_alert = "Enter First Name"
    elif(R_email == ''):
        message_register_alert = "please Enter the Email ID"
    elif(R_category==''):
        message_register_alert="Please Enter Category"
    else:
        error="Null"
        try:
            temp_pass = get_password()
            if(User.objects.filter(username=R_username).exists()):
                message_register_alert = "User Already Exits"
            else:
                user1=User.objects.get(username="kraken")
                user = User.objects.create_user(R_username, R_email, temp_pass)
                print "user created"
                try:
                    notification.objects.create(title="Registered",body="YOU HAVE BEEN REGISTERD Please change your password & Complete your profile",link='/edit',receiver=user,sender=user1)
                except Exception as e:
                    print e
                print temp_pass
                user.first_name = R_fname
                user.last_name = R_lname
                if(R_category=='student'):
                    g = Group.objects.get(name='student')
                    g.user_set.add(user)
                else:
                    g = Group.objects.get(name='faculty')
                    g.user_set.add(user)
                    user.is_active=False
                print "create"
                user.save()
                if(R_category=='student'):
                    student_profile.objects.create(user=user) 
                else:
                    faculty_profile.objects.create(user=user)
                subject = "Confirmation  mail"
                message = "Your password is " + temp_pass
                from_email = settings.EMAIL_HOST_USER
                to_list = [R_email, settings.EMAIL_HOST_USER]
                print "above mail"
                send_mail(subject, message, from_email, to_list, fail_silently=False)
                mail(request,R_email,'mail/email.txt','mail/fancy-1-2-3.html')
                message_register_alert = 'success'
        except Exception as e:
            return HttpResponse(e)
            #message_register_alert = "Error occured in account creation"
            user.delete()
    return message_register_alert


def get_password():
    temp_pass = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        pass_exists = User.objects.get(password=temp_pass)
        get_password()
    except:
        return temp_pass



def reset(request):
    # Wrap the built-in password reset view and pass it the arguments
    # like the template name, email template name, subject template name
    # and the url to redirect after the password reset is initiated.
    return password_reset(request, template_name='accounts/reset.html', post_reset_redirect=reverse('success'))

# This view handles password reset confirmation links. See urls.py file for the mapping.
# This view is not used here because the password reset emails with confirmation links
# cannot be sent from this application.


def reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.

    return password_reset_confirm(request,template_name='accounts/reset_confirm.html', uidb64=uidb64, token=token, post_reset_redirect=reverse('success2'))

# This view renders a page with success message.


def success(request):
    return render(request, 'accounts/success.html')

def success2(request):
    return render(request, 'accounts/changed_successfully.html')

def lock(request):
    return render(request, 'accounts/lock_screen.html')



# password change function
@login_required
def change_password(request):
    if request.method=="POST":
        new_password = request.POST.get('change_password', '')
        if new_password != '':
            request.user.set_password(new_password)
            request.user.save()
            #new_password = make_password(new_password,salt=None,hasher='default')
            # User.objects.select_related().filter(username=request.user.username).update(password=new_password)
            return render(request, 'index.html', {'changed': "password changed successfully"}, context_instance=RequestContext(request))
        else:
            return render(request,'accounts/changepassword.html',{'msg':"Enter new Password"})
    else:
        return render(request,'accounts/changepassword.html',{'msg':"Enter new Password"})
            


def mail(request,receiver,subject,body):
    c = Context({'username': settings.EMAIL_HOST_USER })    
    text_content = render_to_string(subject, c)
    html_content = render_to_string(body, c)

    email = EmailMultiAlternatives('Subject', text_content)
    email.attach_alternative(html_content, "text/html")
    email.to = [receiver]
    email.send()