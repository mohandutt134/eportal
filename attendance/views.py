from django.shortcuts import render

from attendance.models import attendance
from django.contrib.auth.decorators import login_required
from student.models import student_profile, Course , faculty_profile
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
from django.core.exceptions import PermissionDenied
from attendance.models import attendance
from django.db.models import Q
import datetime
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Create your views here.
@login_required
def show_students(request):
	if request.session['type']=='faculty':
		courses = Course.objects.filter(facultyassociated=request.user.faculty_profile).exclude(semester='OPEN')
		if request.method == 'POST':
			if 'search' in request.POST:
				id=request.POST.get('selected_course')
				selected_course = Course.objects.get(course_id=id)
				request.session['selected_id']=id
				students=student_profile.objects.filter(coursetaken=selected_course,Semester=selected_course.semester).order_by('user')
				return render(request,'attendance_form.html',{'courses':courses,'students':students,'selected_course':selected_course})

			elif 'submit' in request.POST:
				selected_course = Course.objects.get(course_id=request.session['selected_id'])
				now=datetime.date.today()
				if attendance.objects.filter(course=selected_course,date=now):
					return render(request,'attendance_form.html',{'courses':courses,'error':"You have already submitted today's attendance"})
				else:
					present_students = request.POST.getlist('present')
					att = attendance.objects.create(course=selected_course)
					for student in present_students:
						std = User.objects.get(username=student)
						s = student_profile.objects.get(user=std)
						att.present.add(s)
					return render(request,'attendance_form.html',{'courses':courses,'success':"Attendance has been submitted successfully"})

		else:
			return render(request,'attendance_form.html',{'courses':courses})
	else:
		raise PermissionDenied

@login_required
def controls(request):
	if request.session['type']=='faculty':
		courses = Course.objects.filter(facultyassociated=request.user.faculty_profile)
		return render(request,'attendance_controls.html',{'courses':courses})
	else:
		raise PermissionDenied

@login_required
def show(request):
	if request.session['type']=='faculty':
		courses = Course.objects.filter(facultyassociated=request.user.faculty_profile).exclude(semester='OPEN')
		temp='base/sidebarf.html'
	else:
		courses = request.user.student_profile.coursetaken.all()
		temp='base/sidebars.html'
	if request.method == 'POST':
		if 'search' in request.POST:
			id=request.POST.get('selected_course')
			selected_course = Course.objects.get(course_id=id)
			total = attendance.objects.filter(course=selected_course).count()
			request.session['selected_id']=id
			students=student_profile.objects.filter(coursetaken=selected_course,Semester=selected_course.semester).order_by('user')
			return render(request,'attendance_result.html',{'temp':temp,'courses':courses,'students':students,'selected_course':selected_course,'total':total})

	else:
		return render(request,'attendance_result.html',{'temp':temp,'courses':courses})

