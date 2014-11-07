from django.shortcuts import render
from django.shortcuts import render_to_response
from course.form import CourseForm
# Create your views here.
def course(request):
	form=CourseForm()
	return render_to_response("course.html",{"form":form})
