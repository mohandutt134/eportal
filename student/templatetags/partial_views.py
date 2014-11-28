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


