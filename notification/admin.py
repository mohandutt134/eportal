from django.contrib import admin

# Register your models here.
from notification.models import notification,activity,message
admin.site.register(notification)
admin.site.register(activity)
admin.site.register(message)