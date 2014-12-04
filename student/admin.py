from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from student.models import Course,student_profile,faculty_profile,material


class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Course

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm

class FacultyAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = faculty_profile

class FacultyAdmin(admin.ModelAdmin):
    form = FacultyAdminForm

class materialAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = material

class materialAdmin(admin.ModelAdmin):
    form = materialAdminForm

admin.site.register(Course, CourseAdmin)
admin.site.register(student_profile)
admin.site.register(faculty_profile,FacultyAdmin)
admin.site.register(material,materialAdmin)
