from django import template
from student.models import Course,faculty_profile
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