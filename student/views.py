from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from attendance.models import Attendance
from eportal.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from student.form import *
from django.http import HttpResponse
from notification.models import notification, activity, message
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from quiz.models import *


def handle_uploaded_file(f, uname, path):
    f.name = uname + ".jpg"
    print uname
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(f.name)), 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()


def home(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        courses = Course.objects.all().order_by('?')[:3]
        return render(request, 'index.html', {'courses': courses})


@login_required
def add_material(request, id=None):
    if request.session['type'] == 'faculty':
        try:
            course = Course.objects.get(course_id=id)
            if course.facultyassociated == request.user.faculty_profile:
                if request.method == 'POST':
                    if 'save' in request.POST:
                        form = add_material_form(request.POST, request.FILES)
                        print form
                        if form.is_valid():
                            j = form.save(commit=False)
                            course = Course.objects.get(course_id=id)
                            j.course = course
                            j.addedby = request.user
                            j.save()
                            subject = "New Material Added: " + j.title
                            activity.objects.create(subject=subject, course=course)
                            students = student_profile.objects.filter(coursetaken=course)
                            link = '/courses/' + id
                            for student in students:
                                notification.objects.create(title="Course Update", body="New Material has been added",
                                                            link=link, course=course, receiver=student.user,
                                                            sender=request.user)
                            return redirect('course', id=id)
                        else:
                            print form.errors
                            return render(request, 'add_material.html', {'form': form})
                else:
                    form = add_material_form()
                    return render(request, 'add_material.html', {'form': form})
            else:
                raise PermissionDenied
        except Exception as e:
            return HttpResponse(e)


def pprofile(request, username=None):
    try:
        username = username.upper()
        usr = User.objects.get(username=username)
        if usr.is_active:
            if request.user.is_authenticated():
                if request.user.groups.filter(name='faculty').exists():
                    return render(request, 'pprofile.html', {'temp': 'base/sidebarf.html', 'usr': usr})
                else:
                    return render(request, 'pprofile.html', {'temp': 'base/sidebars.html', 'usr': usr})
            else:
                return render(request, 'pprofile.html', {'temp': 'base/header.html', 'usr': usr})
        else:
            return render(request, '404.html')
    except Exception, e:
        return HttpResponse(e)


@login_required
def courses(request):
    if request.session.get('type', None) == 'faculty':
        try:
            faculty = faculty_profile.objects.get(user=request.user)
            courses = Course.objects.get(facultyassociated=faculty)
        except:
            return render(request, '404.html')
        return render(request, 'courses.html', {'temp': 'base/sidebarf.html', 'courses': courses})
    else:
        return redirect('dashboard')


@login_required
def course(request, id=None):
    if request.session.get('type', None) == 'faculty':
        try:
            course = Course.objects.get(course_id=id)
            if course.facultyassociated == request.user.faculty_profile:
                activities = activity.objects.filter(course=course)
                return render(request, 'admin_course_view.html', {'course': course, 'activities': activities})
            else:
                return render(request, '403.html')

        except Exception as e:
            return render(request, '404.html')
    else:
        try:
            course = Course.objects.get(course_id=id)
            if course in request.user.student_profile.coursetaken.all():
                activities = activity.objects.filter(course=course)
                materials = material.objects.filter(course=course)
                total = Attendance.objects.filter(course=course).count()
                quiz = quiz_spec.objects.filter(course=course)
                total_p = Attendance.objects.filter(course=course, present=request.user.student_profile).count()
                anns = announcement.objects.filter(course=course).order_by('-created_at')
                videos = video.objects.filter(course=course).order_by('-posted_at')
                return render(request, 'student_course.html',
                              {'course': course, 'activities': activities, 'materials': materials, 'total': total,
                               'total_p': total_p, 'quizes': quiz, 'anns': anns, 'videos': videos})
            else:
                raise PermissionDenied
        except Exception as e:
            return HttpResponse(e)


def allcourses(request):
    temp = 'base/header.html'
    if 'type' in request.session:
        if request.session.get('type', None) == 'faculty':
            temp = 'base/sidebarf.html'
        else:
            temp = 'base/sidebars.html'

    if request.method == 'POST':
        if 'search' in request.POST:
            string = request.POST.get('search_string')
            courses = Course.objects.filter(course_name__icontains=string)
            return render(request, 'public_courses.html', {'temp': temp, 'courses': courses})

        elif 'category' in request.POST:
            dept = request.POST.get('department')
            sem = request.POST.get('semester')
            if sem == 'all':
                courses = Course.objects.filter(dept=dept)
            else:
                courses = Course.objects.filter(dept=dept, semester=sem)
            return render(request, 'public_courses.html', {'temp': temp, 'courses': courses})
        else:
            raise PermissionDenied
    else:
        courses = Course.objects.filter(dept='CSE')
        return render(request, 'public_courses.html', {'temp': temp, 'courses': courses})


@login_required
def dashboard(request):
    faculty_cse = faculty_profile.objects.filter(department="CSE")
    faculty_ece = faculty_profile.objects.filter(department="ECE")
    faculty_mec = faculty_profile.objects.filter(department="MEC")
    faculty_ibt = faculty_profile.objects.filter(department="IBT")
    notifications = notification.objects.filter(receiver=request.user, viewed=True).order_by('-time')[0:10]
    messages = message.objects.filter(receiver=request.user, viewed=True).order_by('-time')[0:10]
    type = request.session.get('type', None)
    if type is None:
        return redirect('/admin')
    else:
        if type == 'faculty':
            courses = Course.objects.filter(facultyassociated=request.user.faculty_profile)
            return render(request, 'dashboard.html',
                          {'temp': 'base/sidebarf.html', 'courses': courses, 'faculty_cse': faculty_cse,
                           'faculty_ece': faculty_ece, 'faculty_mec': faculty_mec, 'faculty_ibt': faculty_ibt,
                           'notifications': notifications, 'messages': messages}, )

        else:
            courses = request.user.student_profile.coursetaken.all()
            return render(request, 'dashboard.html',
                          {'temp': 'base/sidebars.html', 'courses': courses, 'faculty_cse': faculty_cse,
                           'faculty_ece': faculty_ece, 'faculty_mec': faculty_mec, 'faculty_ibt': faculty_ibt,
                           'notifications': notifications, 'messages': messages})


def about(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name='faculty').exists():
            return render(request, 'template.html', {'temp': 'base/sidebarf.html'})
        else:
            return render(request, 'template.html', {'temp': 'base/sidebars.html'})
    else:
        return render(request, 'template.html', {'temp': 'base/header.html'})


@login_required
def profile_edit(request):
    uname = request.POST.get('username', '')
    fname = request.POST.get('first_name', '')
    lname = request.POST.get('last_name', '')
    dept = request.POST.get('department', '')
    rsrch = request.POST.get('research', '')
    aoi = request.POST.get('aoi', '')
    des = request.POST.get('description', '')
    web = request.POST.get('weburl', '')
    User.objects.filter(username=uname).update(first_name=fname, last_name=lname)

    faculty_profile.objects.filter(user=User.objects.get(username=uname)).update(department=dept, description=des,
                                                                                 research=rsrch, areaofinterest=aoi,
                                                                                 weburl=web)
    return redirect('/profile')


@login_required
def profile_edit_student(request):
    uname = request.POST.get('username', '')
    fname = request.POST.get('first_name', '')
    lname = request.POST.get('last_name', '')
    dept = request.POST.get('department', '')
    rsrch = request.POST.get('research', '')
    aoi = request.POST.get('aoi', '')
    des = request.POST.get('description', '')
    web = request.POST.get('weburl', '')
    User.objects.filter(username=uname).update(first_name=fname, last_name=lname)

    faculty_profile.objects.filter(user=User.objects.get(username=uname)).update(department=dept, description=des,
                                                                                 research=rsrch, areaofinterest=aoi,
                                                                                 weburl=web)
    return redirect('/profile')


def changePassword(request):
    redirect_to = request.GET.get('next', '')
    if 'change_password_submit' in request.POST:
        old_password = request.POST.get('old_password', '')
        if request.user.check_password(old_password):
            new_password = request.POST.get('new_password', '')
            if new_password != '':
                request.user.set_password(new_password)
                request.user.save()
                notification.objects.create(title="Confirmation", body="Password Changed Successfully", link="#",
                                            receiver=request.user, sender=request.user)
        else:
            notification.objects.create(title="Error", body="Wrong old password", link="#", receiver=request.user,
                                        sender=request.user)
            return redirect(redirect_to)
    return redirect(redirect_to)


@login_required
def profile(request):
    if request.method == 'POST':
        uname = request.POST.get('username', '')
        fname = request.POST.get('first_name', '')
        salutation = request.POST.get('salutation', '')
        lname = request.POST.get('last_name', '')
        User.objects.filter(username=uname).update(first_name=fname, last_name=lname)
        if 'department' in request.POST:
            dept = request.POST.get('department', '')
            rsrch = request.POST.get('research', '')
            aoi = request.POST.get('aoi', '')
            des = request.POST.get('description', '')
            web = request.POST.get('weburl', '')
            image = request.FILES.get('image', '')
            if image:
                handle_uploaded_file(image, request.user.username, 'fpp/')
            # print image.name
            else:
                image = request.user.faculty_profile.image
            print image
            faculty_profile.objects.filter(user=User.objects.get(username=uname)).update(salutation=salutation,
                                                                                         department=dept,
                                                                                         description=des,
                                                                                         research=rsrch,
                                                                                         areaofinterest=aoi, weburl=web,
                                                                                         image=image)
            # return render(request,'profile.html',{'temp':'base/sidebarf.html','msg':"Profile has been successfully updated"})
            return redirect('profile')
        else:
            brnch = request.POST.get('branch', '')
            sem = request.POST.get('sem', '')
            dob = request.POST.get('dateofbirth', '')
            image = request.FILES.get('dp', '')
            if image:
                handle_uploaded_file(image, request.user.username, 'fpp/')
            # print image.name
            else:
                image = request.user.student_profile.image
            print image
            student_profile.objects.filter(user=User.objects.get(username=uname)).update(salutation=salutation,
                                                                                         Branch=brnch, Semester=sem,
                                                                                         image=image)
            return redirect('profile')
            # return render(request,'student_profile.html',{'temp':'base/sidebars.html','msg':"Profile has been successfully updated"})
    else:
        if request.user.groups.filter(name='faculty').exists():
            form = update_faculty_image()
            return render(request, 'profile.html', {'temp': 'base/sidebarf.html', 'form': form})
        else:
            form = update_student_image()
            return render(request, 'student_profile.html', {'temp': 'base/sidebars.html', 'form': form})


def course_info(request, id):
    try:
        course = Course.objects.get(course_id=id)
        similar_courses = Course.objects.filter(dept=course.dept).exclude(course_id=id)[:3]
        if 'type' in request.session:
            if request.session['type'] == 'student':
                count = student_profile.objects.filter(user=request.user, coursetaken=course).count()
                return render(request, 'courseinfo.html',
                              {'temp': 'base/sidebars.html', 'course': course, 'count': count,
                               'similar_courses': similar_courses})
            else:
                return render(request, 'courseinfo.html',
                              {'temp': 'base/sidebarf.html', 'course': course, 'faculty': "isfaculty",
                               'similar_courses': similar_courses})
        return render(request, 'courseinfo.html',
                      {'temp': 'base/header.html', 'course': course, 'similar_courses': similar_courses})
    except Exception as e:
        return HttpResponse(e)


def faculties(request):
    temp = 'base/header.html'
    if 'type' in request.session:
        if request.session['type'] == 'faculty':
            temp = 'base/sidebarf.html'
        else:
            temp = 'base/sidebars.html'

    if request.method == 'POST':
        if 'category' in request.POST:
            dept = request.POST.get('department')
            faculties = faculty_profile.objects.filter(department=dept)
            return render(request, 'faculty_list.html', {'temp': temp, 'faculties': faculties})
        else:
            raise PermissionDenied
    else:
        faculties = faculty_profile.objects.filter(department='CSE')
        return render(request, 'faculty_list.html', {'temp': temp, 'faculties': faculties})


@login_required
@csrf_exempt
def course_register(request):
    if request.method == 'POST':
        course = Course.objects.get(course_id=request.POST.get('id'))
        request.user.student_profile.coursetaken.add(course)
        return HttpResponse('success')
    else:
        raise PermissionDenied


def contactview(request):
    temp = 'base/header.html'
    if 'type' in request.session:
        if request.session['type'] == 'faculty':
            temp = 'base/sidebarf.html'
        else:
            temp = 'base/sidebars.html'

    if request.method == 'POST':
        name = request.POST.get('name', '')
        subject = request.POST.get('topic', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        if subject and message and from_email:
            datatuple = (
                ('Query mail :' + subject, "This is a mail from " + name + from_email + message,
                 settings.EMAIL_HOST_USER, ['vibhanshu86@gmail.com']),
                ('Reply :' + subject, "Your query has been logged to us ", settings.EMAIL_HOST_USER, [from_email]),
            )
            try:
                send_mass_mail(datatuple)
            except Exception, e:
                return HttpResponse(e)
            return render(request, 'thankyou.html', {'temp': temp})
        else:
            return HttpResponse("fill all the fields")

    else:
        return render(request, 'contacts.html', {'temp': temp})


@login_required
def mail(request):
    receiver = "vibhanshu86@gmail.com"
    send_mail("Subject", "Message", settings.EMAIL_HOST_USER, [receiver])
    return HttpResponse("success")
    # receiver="vibhanshu86@gmail.com"
    # subject="mail/email.txt"
    # body="mail/email.html"
    # c = Context({'username': settings.EMAIL_HOST_USER })    
    # text_content = render_to_string(subject, c)
    # html_content = render_to_string(body, c)

    # email = EmailMultiAlternatives('Subject', text_content)
    # email.attach_alternative(html_content, "text/html")
    # email.to = [receiver]
    # email.send()


@login_required
def add_ann(request):
    if request.session['type'] == 'faculty':
        # try:
        if request.method == 'POST':
            if 'save' in request.POST:
                print 'hello'
                form = annForm(request.POST)
                form.fields["course"].queryset = Course.objects.filter(facultyassociated=request.user.faculty_profile)
                if form.is_valid():
                    form.save()
                    subject = "New Announcement"
                    course = form.cleaned_data['course']
                    activity.objects.create(subject=subject, course=course)
                    students = student_profile.objects.filter(coursetaken=course)
                    link = '/courses/' + course.course_id
                    for student in students:
                        notification.objects.create(title="Course Update", body="New Announcement", link=link,
                                                    course=course, receiver=student.user, sender=request.user)
                    return redirect('course', id=course.course_id)
                else:
                    print form.errors
                    return render(request, 'add_ann.html', {'form': form})
            raise PermissionDenied
        else:
            form = annForm()
            form.fields["course"].queryset = Course.objects.filter(facultyassociated=request.user.faculty_profile)
            return render(request, 'add_ann.html', {'form': form})
        # except Exception as e:
        # return HttpResponse(e)
    else:
        raise PermissionDenied


@login_required
def add_video(request):
    if request.session['type'] == 'faculty':
        # try:
        if request.method == 'POST':
            if 'save' in request.POST:
                print 'hello'
                form = videoForm(request.POST)
                form.fields["course"].queryset = Course.objects.filter(facultyassociated=request.user.faculty_profile)
                if form.is_valid():
                    form.save()
                    subject = "New Video"
                    course = form.cleaned_data['course']
                    activity.objects.create(subject=subject, course=course)
                    students = student_profile.objects.filter(coursetaken=course)
                    link = '/courses/' + course.course_id
                    for student in students:
                        notification.objects.create(title="Course Update", body="New Video", link=link, course=course,
                                                    receiver=student.user, sender=request.user)
                    return redirect('course', id=course.course_id)
                else:
                    print form.errors
                    return render(request, 'add_video.html', {'form': form})
            raise PermissionDenied
        else:
            form = videoForm()
            form.fields["course"].queryset = Course.objects.filter(facultyassociated=request.user.faculty_profile)
            return render(request, 'add_video.html', {'form': form})
        # except Exception as e:
        # return HttpResponse(e)
    else:
        raise PermissionDenied


@login_required
def add_syllabus(request, id):
    if request.session['type'] == 'faculty':
        try:
            course = Course.objects.get(course_id=id)
            if course.facultyassociated == request.user.faculty_profile:
                if request.method == 'POST':
                    if 'save' in request.POST:
                        s = get_object_or_404(Course, pk=Course.objects.get(course_id=id).course_id)
                        form = syllabusForm(request.POST, instance=s)
                        if form.is_valid():
                            form.save()
                            subject = "Course Update"
                            activity.objects.create(subject=subject, course=course)
                            students = student_profile.objects.filter(coursetaken=course)
                            link = '/courseinfo/' + course.course_id
                            for student in students:
                                notification.objects.create(title="Course Update", body="Syllabus Updated", link=link,
                                                            course=course, receiver=student.user, sender=request.user)
                            return redirect('course', id=course.course_id)
                        else:
                            print form.errors
                            return render(request, 'add_syllabus.html', {'form': form})

                    else:
                        return redirect('dashboard')
                else:
                    course = Course.objects.get(course_id=id)
                    s = get_object_or_404(Course, pk=Course.objects.get(course_id=id).course_id)
                    form = syllabusForm(instance=s)
                    # form.syllabus=Course.objects.get(course_id=id).syllabus
                    return render(request, 'add_syllabus.html', {'form': form, 'course': course})
            else:
                return render(request, '403.html')
        except:
            return render(request, '404.html')
    else:
        raise PermissionDenied
