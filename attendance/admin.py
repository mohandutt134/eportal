from django.contrib import admin


from attendance.models import Attendance
from django_extensions.admin import ForeignKeyAutocompleteAdmin


#admin.site.register(attendance)


class Attendance_Admin(ForeignKeyAutocompleteAdmin):
    # User is your FK attribute in your model
    # first_name and email are attributes to search for in the FK model
    related_search_fields = {
       'course': ('course_name',),
    }

    fields = ( 'date' ,'course', 'present', )

admin.site.register(Attendance, Attendance_Admin)

