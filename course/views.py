from django.shortcuts import render
from django.shortcuts import render_to_response
from course.form import CourseForm
from django.core.files.base import File
from course.models import course
from django.db.models import Q
from django.core.context_processors import csrf
# Create your views here.
def course(request):
	if(request.method == 'POST'):
		course_id1 = request.POST.get('course_id', '')
		course_name1 = request.POST.get('course_name', '')
		credits1 = request.POST.get('credits', '')
		end_date1=request.POST.get('end_date', '')
		start_date1=request.POST.get('start_date', '')
		image1=request.FILES.get('image','')
		image2=request.FILES.get('image').name
		course_data=course(
			courseid=course_id1,
			coursename=course_name1,
			startdate=start_date1,
			enddate=end_date1,
			image=image2,
			credits=credits1
		)
		course_data.save()

		
	else:
		form=CourseForm()	
	return render(request,'course.html',{'form':form})

									