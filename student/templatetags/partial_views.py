from django import template
from student.models import Course,faculty_profile,student_profile
from django.contrib.auth.models import User
from django.core import serializers

register = template.Library()
@register.inclusion_tag('course_list.html',takes_context=True)
def course_list_function(context):
    try:
        courses = Course.objects.filter(facultyassociated=context['request'].user.faculty_profile)
    except:
        courses=None
        print "exception occured"
    return {'courses':courses}

@register.inclusion_tag('bar.html')
def make_bar(course):
	course=Course.objects.get(course_id=course.course_id)
	count=student_profile.objects.filter(coursetaken=course).count()
	return{'count':count}
	#courses = Course.objects.get(course_id=context['id'])
    
    #count=student_profile.objects.filter(coursetaken=course).count()
   	#return {'count':count}

@register.inclusion_tag('course_code.html',takes_context=True)
def expansion(context):
    if context['usr'].groups.filter(name='faculty').exists():
        code = context['usr'].faculty_profile.department
    else:
        code = context['usr'].student_profile.Branch
    print code
    print "below code"
    expanded = 'OTHER'
    if code == 'CSE':
        expanded = "Computer Science & Engineering"
    if code == "ECE":
        expanded = "Electronics & Communication Engineering"
    if code == "MEC":
        expanded = "Mechanical Engineering"
    if code == "IBT":
        expanded = "Industrial Biotechnology"
    return {'expanded':expanded}
