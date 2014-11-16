from django.db import models
from django.contrib.auth.models import User
from student.models import Course
# Create your models here.

class notification(models.Model):
	title = models.CharField(max_length=256)
	body = models.TextField()
	viewed = models.BooleanField(default=False)
	link = models.CharField(max_length=256)
	course = models.ForeignKey(Course)
	sender = models.ForeignKey(User,related_name="sends", related_query_name="send")
	receiver = models.ForeignKey(User,related_name="tags", related_query_name="tag")
	time=models.DateTimeField(auto_now=True)

	def __unicode__(self):
   		return unicode(self.title) or u''



