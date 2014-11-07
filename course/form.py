from django import forms
from student.models import Course

class CourseForm(forms.ModelForm):
	course_id=forms.CharField(max_length=30,help_text="Please Enter the course_id")
	course_name=forms.CharField(max_length=30)
	srart_date= forms.DateField()
	end_date=forms.DateField()
	credits=forms.IntegerField()
	image = forms.FileField()

