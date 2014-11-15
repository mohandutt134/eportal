from django.forms import ModelForm
from student.models import student
class student_form(ModelForm):
	class Meta:
		model=student
		fields = ['branch', 'image', 'dateofbirth']