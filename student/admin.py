from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from student.models import *


class CourseAdminForm(forms.ModelForm):
    syllabus = forms.CharField(widget=CKEditorWidget(config_name='admin_ckeditor'))

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm


class FacultyAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='admin_ckeditor'))

    class Meta:
        model = faculty_profile
        fields = '__all__'


class FacultyAdmin(admin.ModelAdmin):
    form = FacultyAdminForm


class materialAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='admin_ckeditor'))

    class Meta:
        model = material
        fields = '__all__'


class materialAdmin(admin.ModelAdmin):
    form = materialAdminForm


class announcementAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(config_name='admin_ckeditor'))

    class Meta:
        model = announcement
        fields = '__all__'


class announcementAdmin(admin.ModelAdmin):
    form = announcementAdminForm


class videoAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(config_name='admin_ckeditor'))

    class Meta:
        model = video
        fields = '__all__'



class videoAdmin(admin.ModelAdmin):
    form = videoAdminForm


admin.site.register(Course, CourseAdmin)
admin.site.register(student_profile)
admin.site.register(faculty_profile, FacultyAdmin)
admin.site.register(material, materialAdmin)
admin.site.register(announcement, announcementAdmin)
admin.site.register(video, videoAdmin)
