from django.db import models

# Create your models here.
class student(models.Model):
	username=models.EmailField(primary_key=True)
	FirstName=models.CharField(max_length=50)
	LastNmae=models.CharField(max_length=50,default=None)
	DOB=models.CharField(max_length=20,default=None)
	Branch=models.CharField(max_length=10,default=None)
	Semester=models.CharField(max_length=10,default=None)
	image = models.CharField(max_length=20)

class Course(models.Model):
	course_id=models.CharField(max_length=20,primary_key=True)
	course_name=models.CharField(max_length=20)
	start_date=models.DateField()
	end_date=models.DateField()
	credits=models.IntegerField()
	image = models.ImageField(
        upload_to='images/', 
        height_field=300, 
        width_field=200
    )
class user(models.Model):
 	username=models.EmailField(primary_key=True)
 	password=models.CharField(max_length=50)
 	status=models.BooleanField(default=False)

class coursetaken(models.Model):
	username= models.ForeignKey(student)
	course_id=models.ForeignKey(Course)
	credit=models.CharField(max_length=10)
	
	