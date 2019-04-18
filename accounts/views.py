import uuid
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from notification.models import notification
from student.models import faculty_profile, student_profile
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


def login_view(request, next='home'):
    if request.user.is_authenticated():
        return redirect('home')

    if 'login' in request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.GET.get('next')
                if request.user.groups.filter(name='faculty').exists():
                    request.session['type'] = 'faculty'
                elif request.user.groups.filter(name='student').exists():
                    request.session['type'] = 'student'
                if next:
                    return redirect(next)
                elif user.is_staff:
                    return redirect('/admin')
                else:
                    return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'message_login': "Your account is inactive"})
        else:
            return render(request, 'accounts/login.html', {'message_login': "Wrong username or password"})
    if 'register' in request.POST:
        # call registration function
        message = registration_function(request)  # store message from registration function
        return render(request, 'accounts/login.html', {'message_register_alert': message})

    return render(request, 'accounts/login.html', {'message_register_alert': ''})


def logout_view(request):
    logout(request)
    return redirect('home')


def register2(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":
        msg = registration_function(request)
        return render(request, 'accounts/register.html', {"msg": msg})
    else:
        return render(request, 'accounts/register.html')


def registration_function(request):
    R_fname = request.POST.get('R_fname', '')
    R_lname = request.POST.get('R_lname', '')
    R_email = request.POST.get('R_email', '')
    R_category = request.POST.get('category', '')
    R_password = request.POST.get('password', '')
    if R_email == '':
        message_register_alert = "Enter username"
    elif R_password == '':
        message_register_alert = "Enter password"
    elif R_fname == '':
        message_register_alert = "Enter first name"
    elif R_category == '':
        message_register_alert = "Please choose category"
    else:
        try:
            if User.objects.filter(username=R_email).exists():
                message_register_alert = "User already exits"
            else:
                user1 = User.objects.get(username='admin')
                user = User.objects.create_user(R_email, R_email, R_password)
                try:
                    notification.objects.create(title="Registered",
                                                body="YOU HAVE BEEN REGISTERED."
                                                     "Please change your password & Complete your profile",
                                                link='/profile', receiver=user, sender=user1)
                except Exception as e:
                    print e
                user.first_name = R_fname
                user.last_name = R_lname
                if R_category == 'student':
                    g = Group.objects.get(name='student')
                    g.user_set.add(user)
                else:
                    g = Group.objects.get(name='faculty')
                    g.user_set.add(user)
                    user.is_active = False
                user.save()
                if R_category == 'student':
                    student_profile.objects.create(user=user)
                else:
                    faculty_profile.objects.create(user=user)
                # subject = "Confirmation  mail"
                # message = "Your account has been created"
                # from_email = settings.EMAIL_HOST_USER
                # to_list = [R_email, settings.EMAIL_HOST_USER]
                # send_mail(subject, message, from_email, to_list, fail_silently=False)
                # mail(request,R_email,'mail/email.txt','mail/fancy-1-2-3.html')
                message_register_alert = 'success'
        except Exception as e:
            return HttpResponse(e)
    return message_register_alert


def get_password():
    return str(uuid.uuid4())[:11].replace('-', '')


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

    return password_reset_confirm(request, template_name='accounts/reset_confirm.html', uidb64=uidb64, token=token,
                                  post_reset_redirect=reverse('success2'))


# This view renders a page with success message.


def success(request):
    return render(request, 'accounts/success.html')


def success2(request):
    return render(request, 'accounts/changed_successfully.html')


def lock(request):
    return render(request, 'accounts/lock_screen.html')


# password change function
# @login_required
# def change_password(request):
#     if request.method=="POST":
#         new_password = request.POST.get('change_password', '')
#         if new_password != '':
#             request.user.set_password(new_password)
#             request.user.save()
#             #new_password = make_password(new_password,salt=None,hasher='default')
#             # User.objects.select_related().filter(username=request.user.username).update(password=new_password)
#             return render(request, 'index.html', {'changed': "password changed successfully"}, context_instance=RequestContext(request))
#         else:
#             return render(request,'accounts/changepassword.html',{'msg':"Enter new Password"})
#     else:
#         return render(request,'accounts/changepassword.html',{'msg':"Enter new Password"})


def mail(request, receiver, subject, body):
    c = Context({'username': settings.EMAIL_HOST_USER})
    text_content = render_to_string(subject, c)
    html_content = render_to_string(body, c)

    email = EmailMultiAlternatives('Subject', text_content)
    email.attach_alternative(html_content, "text/html")
    email.to = [receiver]
    email.send()
