from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
	course_id=models.CharField(max_length=10)
	course_name=models.CharField(max_length=10)
	start_date=models.DateField(max_length=10)
	end_date=models.DateField(max_length=10)
	image=models.CharField(max_length=10)
	credits=models.CharField(max_length=10)

    #def __str__(self):
 		#return self.course_id

class student(models.Model):
	username=models.EmailField(primary_key=True)
	FirstName=models.CharField(max_length=50)
	LastName=models.CharField(max_length=50,default=None)
	DOB=models.CharField(max_length=20,default=None)
	Branch=models.CharField(max_length=10,default=None)
	Semester=models.CharField(max_length=10,default=None)
	image = models.CharField(max_length=20)
	coursetaken=models.ManyToManyField(Course)

	def __str__(self):
		return self.username



class user(models.Model):
 	username=models.EmailField(primary_key=True)
 	password=models.CharField(max_length=100)
 	status=models.BooleanField(default=False)

 	def __str__(self):
 		return self.username
	
	