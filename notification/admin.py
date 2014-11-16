from django.contrib import admin

# Register your models here.
from notification.models import notification
admin.site.register(notification)