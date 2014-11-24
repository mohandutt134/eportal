from django.contrib import admin
from student import models
#from django_markdown.admin import MarkdownModelAdmin



class faculty_profileAdmin(admin.ModelAdmin):
    # fields display on change list
    list_display = ['title', 'text']
    # fields to filter the change list with
    save_on_top = True
    # fields to search in change list
    prepopulated_fields = {"weburl":("department",)}
    search_fields = ['title', 'text']
    # enable the date drill down on change list
    date_hierarchy = 'pub_date'

admin.site.register(faculty_profileAdmin)