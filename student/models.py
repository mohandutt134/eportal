from django.db import models
from django.contrib.auth.models import User
from time import time
# Create your models here.
def get_upload_file_name(instance,filename):
    return "material/%s_%s" % (str(time()).replace('.','_'),filename)

class faculty_profile(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    department=models.CharField(max_length=25)
    facultyrating=models.CharField(max_length=5)
    areaofinterest=models.CharField(max_length=40)
    research=models.CharField(max_length=50)
    description=models.TextField()
    weburl=models.CharField(max_length=250)
    image=models.ImageField(upload_to='fpp',default='/static/uploaded_image/user_blue.png')

    
    def __str__(self):
        return self.user.username

class Course(models.Model):
    CHOICES = (
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('MEC', 'MEC'),
        ('IBT', 'IBT'),
        ('OTHER','OTHER')
    )
    CHOICES_SEM = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('OPEN', 'OPEN')

    )
    course_id=models.CharField(max_length=10,primary_key=True)
    course_name=models.CharField(max_length=50)
    dept=models.CharField(max_length=5,choices=CHOICES,default='OTHER')
    description=models.TextField(default="There is no description")
    start_date=models.DateField()
    end_date=models.DateField()
    semester=models.CharField(max_length=4,choices=CHOICES_SEM,default='OPEN')
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


class material(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(default="There is no Description")
    course=models.ForeignKey(Course)
    timestamp=models.DateTimeField(auto_now=True)
    addedby=models.ForeignKey(User)
    document=models.FileField(upload_to='material')

    def __unicode__(self):
        return unicode(self.title) or u''


#User.profile=property(lambda u: student_profile.objects.get_or_create(user=u)[0])


User.profile=property(lambda u: student.objects.get_or_create(u=u)[0])

class material(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(default="There is no Description")
    course=models.ForeignKey(Course)
    timestamp=models.DateTimeField(auto_now=True)
    addedby=models.ForeignKey(User)
    document=models.FileField(upload_to=get_upload_file_name)

    def __unicode__(self):
        return unicode(self.title) or u''
