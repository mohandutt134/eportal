from django.db import models
from student.models import student_profile,Course,faculty_profile
from django.contrib.auth.models import User




# model for quiz specification

class quiz_spec(models.Model):
	title=models.TextField()
	course = models.ForeignKey(Course)
	start_date = models.DateField()
	end_date = models.DateField()
	duration = models.IntegerField()
	no_Questions=models.IntegerField()
	credit=models.IntegerField()
	addedBy=models.ForeignKey(faculty_profile)

	def __str__(self):
		return self.title

# model for questions
class question(models.Model):
	CHOICES = (
	    ('option 1','a'),
	    ('option 2','b'),
	    ('option 3','c'),
	    ('option 4','d'),
	)
	statement = models.TextField()
	a = models.TextField()
	b = models.TextField()
	c = models.TextField()
	d = models.TextField()
	addedBY=models.ForeignKey(faculty_profile,null=True)
	ans = models.CharField(max_length=1,choices=CHOICES)
	category=models.TextField()
	extra_info=models.TextField()
	quizes = models.ManyToManyField(quiz_spec,blank=True,null=True)
	dateAdded = models.DateTimeField(auto_now=True); 

	def __str__(self):
		return self.statement

#model for results of students

class result(models.Model):
	user = models.ForeignKey(student_profile)
	course = models.ForeignKey(Course)
	quiz = models.ForeignKey(quiz_spec)
	score = models.IntegerField()

	def __str__(self):
		return self.user.user.username
