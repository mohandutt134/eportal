from django.forms import ModelForm
from student.models import student_profile,faculty_profile

class student_profile_form(ModelForm):
	class Meta:
		model=student_profile
		fields=['DOB','Branch','Semester','image','coursetaken']

class faculty_profile_form(ModelForm):
	class Meta:
		model=faculty_profile
		fields=['department','facultyrating','areaofinterest','research','description','weburl','image']
