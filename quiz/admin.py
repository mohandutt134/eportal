from django.contrib import admin

from quiz.models import question,quiz_spec,result
admin.site.register(question)
admin.site.register(quiz_spec)
admin.site.register(result)