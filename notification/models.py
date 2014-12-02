from django.db import models
from django.contrib.auth.models import User
from student.models import Course
# Create your models here.

class notification(models.Model):
	n_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=256)
	body = models.TextField()
	viewed = models.BooleanField(default=False)
	link = models.CharField(max_length=256)
	course = models.ForeignKey(Course,blank=True,null=True)
	courseName = models.CharField(max_length=256)
	sender = models.ForeignKey(User,related_name="sends", related_query_name="send")
	senderName = models.CharField(max_length=256)
	receiver = models.ForeignKey(User,related_name="tags", related_query_name="tag")
	time=models.DateTimeField(auto_now=True)

	def __unicode__(self):
   		return unicode(self.title) or u''

	class Meta:
		verbose_name = "Notification"
		verbose_name_plural = "Notifications"
		ordering = ["-time"]


class activity(models.Model):
	subject = models.CharField(max_length=256)
	time = models.DateTimeField(auto_now=True)
	course = models.ForeignKey(Course)

	def __unicode__(self):
   		return unicode(self.subject) or u''
   	class Meta:
		verbose_name = "Activity"
		verbose_name_plural = "Activities"
		ordering = ["-time"]

class message(models.Model):
	m_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=256)
	body = models.TextField()
	viewed = models.BooleanField(default=False)
	sender = models.ForeignKey(User,related_name="msends", related_query_name="msend")
	senderName=models.CharField(max_length=256,default="Admin")
	senderImage=models.CharField(max_length=256,default="fpp/user_blue.png")
	receiver = models.ForeignKey(User,related_name="mtags", related_query_name="mtag")
	time=models.DateTimeField(auto_now=True)

	def __unicode__(self):
   		return unicode(self.title) or u''

	class Meta:
		verbose_name = "Message"
		verbose_name_plural = "Messages"
		ordering = ["-time"]
