from django.db import models

# Create your models here.
class course(models.Model):
	courseid=models.CharField(max_length=10)
	coursename=models.CharField(max_length=10)
	startdate=models.CharField(max_length=10)
	enddate=models.CharField(max_length=10)
	image=models.CharField(max_length=10)
	credits=models.CharField(max_length=10)
	

		