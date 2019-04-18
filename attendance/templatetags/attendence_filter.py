from django import template
from student.models import *
from attendance.models import Attendance

register = template.Library()
@register.inclusion_tag('attendance_count_partial.html',takes_context=True)
def get_attendance(context):
    try:
        num = Attendance.objects.filter(course=context['selected_course'], present=context['student']).count()
    	print num
    except:
        num="NA"
        print "exception occured"
    return {'count':num}
