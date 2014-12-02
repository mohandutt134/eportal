from django.db import models
from django.contrib.auth.models import User
from time import time
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
def get_upload_file_name(instance,filename):
    return "material/%s_%s" % (str(time()).replace('.','_'),filename)

def get_upload_image_name(instance,filename):
    return "fpp/%s" % (filename)

class faculty_profile(models.Model):
    CHOICES = (


        ('CSE','CSE'),
        ('ECE','ECE'),
        ('MEC','MEC'),
        ('IBT','IBT')


    )
    user = models.OneToOneField(User,primary_key=True)
    department=models.CharField(max_length=3,choices=CHOICES,default='CSE')
    facultyrating=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0)
    areaofinterest=models.CharField(max_length=40,blank=True)
    research=models.CharField(max_length=50,blank=True)
    description=models.TextField(blank=True)
    weburl=models.CharField(max_length=250,blank=True)

    image=models.ImageField(upload_to=get_upload_image_name,default='user_blue.png')


    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"
        ordering = ["-department"]


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
    image=models.ImageField(upload_to='cpp',default="cpp/course_default.png")
    credits=models.CharField(max_length=10)
    facultyassociated=models.ForeignKey(faculty_profile,blank=True,null=True,related_name='mentor')

    def __str__(self):
        return self.course_name


class student_profile(models.Model):
    CHOICES = (
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('MEC', 'MEC'),
        ('IBT', 'IBT')
    )
    CHOICES_SEM = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
    )
    user = models.OneToOneField(User,primary_key=True)

    DOB=models.DateField(blank=True,null=True)
    Branch=models.CharField(max_length=5,choices=CHOICES,default='CSE')
    Semester=models.CharField(max_length=4,choices=CHOICES_SEM,default='1')
    image = models.ImageField(upload_to='spp',default="user_blue.png")

    coursetaken=models.ManyToManyField(Course,blank=True)

    def __unicode__(self):
        return unicode(self.user) or u''
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["-DOB"]

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
