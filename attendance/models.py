from django.db import models
from django.contrib.auth.models import User
from student.models import student_profile, Course , faculty_profile

class attendance(models.Model):
	a_id = models.AutoField(primary_key=True)
	date = models.DateField(auto_now=True)
	course = models.ForeignKey(Course)
	present = models.ManyToManyField(student_profile)

# Create your models here.
