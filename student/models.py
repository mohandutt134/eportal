from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class faculty_profile(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    department=models.CharField(max_length=25)
    facultyrating=models.CharField(max_length=5)
    areaofinterest=models.CharField(max_length=40)
    research=models.CharField(max_length=50)
    description=models.TextField()
    weburl=models.CharField(max_length=250)
    image=models.ImageField(upload_to='fpp')

    
    def __str__(self):
        return self.user.username

class Course(models.Model):
    course_id=models.CharField(max_length=10,primary_key=True)
    course_name=models.CharField(max_length=50)
    description=models.TextField(default="There is no description")
    start_date=models.DateField()
    end_date=models.DateField()
    semester=models.IntegerField()
    image=models.ImageField(upload_to='cpp')
    credits=models.CharField(max_length=10)
    facultyassociated=models.ForeignKey(faculty_profile,blank=True,null=True,related_name='mentor')

    def __unicode__(self):
        return unicode(self.course_name) or u''


class student_profile(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    DOB=models.DateField()
    Branch=models.CharField(max_length=10,default=None)
    Semester=models.CharField(max_length=10,default=None)
    image = models.ImageField(upload_to='spp')
    coursetaken=models.ManyToManyField(Course)

    def __unicode__(self):
        return unicode(self.user) or u''


#User.profile=property(lambda u: student_profile.objects.get_or_create(user=u)[0])


User.profile=property(lambda u: student.objects.get_or_create(u=u)[0])

