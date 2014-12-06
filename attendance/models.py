from django.db import models
from django.contrib.auth.models import User
from student.models import student_profile, Course , faculty_profile


import datetime

class attendance(models.Model):
	a_id = models.AutoField(primary_key=True)
	date = models.DateField(default=datetime.date.today)
	course = models.ForeignKey(Course)
	present = models.ManyToManyField(student_profile,blank=True)

	def __unicode__(self):
		return unicode(self.date) or u''


# Create your models here.
