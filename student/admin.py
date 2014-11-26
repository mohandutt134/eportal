from django.contrib import admin
from student.models import student_profile,Course,faculty_profile,material
admin.site.register(student_profile)
admin.site.register(Course)
admin.site.register(faculty_profile)
admin.site.register(material)