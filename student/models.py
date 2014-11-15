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
	u=models.OneToOneField(User,null=True)
	sex=models.CharField(max_length=10)
	branch=models.CharField(max_length=10)
	dateofbirth=models.CharField(max_length=20)
	image=models.CharField(max_length=20)
	course_taken=models.ManyToManyField(Course,null=True, blank=True)
	


User.profile=property(lambda u: student.objects.get_or_create(u=u)[0])
	
	