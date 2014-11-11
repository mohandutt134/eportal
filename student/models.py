from django.db import models

# Create your models here.
class Course(models.Model):
	course_id=models.CharField(max_length=20,primary_key=True)
	course_name=models.CharField(max_length=20)
	start_date=models.DateField()
	end_date=models.DateField()
	credits=models.IntegerField()
	#info=models.TextField()
	#instructor=models.ForeignKey()

	image = models.ImageField(
        upload_to='images/', 
        height_field=300, 
        width_field=200
    )

    #def __str__(self):
 		#return self.course_id

class student(models.Model):
	username=models.EmailField(primary_key=True)
	FirstName=models.CharField(max_length=50)
	LastName=models.CharField(max_length=50,default=None)
	DOB=models.CharField(max_length=20,default=None)
	Branch=models.CharField(max_length=10,default=None)
	Semester=models.CharField(max_length=10,default=None)
	image = models.CharField(max_length=20)
	coursetaken=models.ManyToManyField(Course)

	def __str__(self):
		return self.username



class user(models.Model):
 	username=models.EmailField(primary_key=True)
 	password=models.CharField(max_length=100)
 	status=models.BooleanField(default=False)

 	def __str__(self):
 		return self.username
	
	