from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
	course_id=models.CharField(max_length=10,primary_key=True)
	course_name=models.CharField(max_length=10)
	start_date=models.CharField(max_length=10)
	end_date=models.CharField(max_length=10)
	image=models.CharField(max_length=10)
	credits=models.CharField(max_length=10)

    #def __str__(self):
 		#return self.course_id


class student_profile(models.Model):
	user = models.OneToOneField(User,primary_key=True)
	DOB=models.DateField()
	Branch=models.CharField(max_length=10,default=None)
	Semester=models.CharField(max_length=10,default=None)
	image = models.CharField(max_length=20)
	coursetaken=models.ManyToManyField(Course)

	def __unicode__(self):
   		return unicode(self.user) or u''


#User.profile=property(lambda u: student_profile.objects.get_or_create(user=u)[0])


User.profile=property(lambda u: student.objects.get_or_create(u=u)[0])

class faculty_profile(models.Model):
	user = models.OneToOneField(User,primary_key=True)
	department=models.CharField(max_length=25)
	facultyrating=models.CharField(max_length=5)
	areaofinterest=models.CharField(max_length=40)
	research=models.CharField(max_length=50)
	description=models.TextField()
	weburl=models.CharField(max_length=250)
	image=models.CharField(max_length=10)

	
	def __str__(self):
		return 'self.DOB'