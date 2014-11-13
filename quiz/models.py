from django.db import models
from student.models import student,Course
from django.contrib.auth.models import User




# model for quiz specification

class quiz_spec(models.Model):
	course = models.ForeignKey(Course)
	start_date = models.DateField()
	end_date = models.DateField()
	duration = models.IntegerField()

	def __str__(self):
		return self.start_date

# model for questions
class question(models.Model):
	CHOICES = (
	    ('a', 'option 1'),
	    ('b', 'option 2'),
	    ('c', 'option 1'),
	    ('d', 'option 1'),
	)
	statement = models.TextField()
	a = models.TextField()
	b = models.TextField()
	c = models.TextField()
	d = models.TextField()
	ans = models.CharField(max_length=1,choices=CHOICES)
	quizes = models.ManyToManyField(quiz_spec)
	parent = models.ForeignKey(student)
	dateAdded = models.DateTimeField(); 

	def __str__(self):
		return self.statement

#model for results of students

class result(models.Model):
	user = models.ForeignKey(student)
	course = models.ForeignKey(Course)
	quiz = models.ForeignKey(quiz_spec)
	score = models.IntegerField()

	def __str__(self):
		return self.user.username
