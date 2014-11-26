from django.shortcuts import render

#imported from student.views im imports

import uuid
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from student.models import student_profile, Course
from smvdu_portal.settings import MEDIA_ROOT
from django.core.files.base import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
import os
from django.core import serializers
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import Group
from notification.models import notification
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def notificationicon_create(request):
	if(request.method=='POST'):
		data = {'foo': 'bar', 'hello': 'world'}
		data=notification.objects.filter(receiver=request.user,viewed=False)
		data=serializers.serialize("json",data)
		print data
		return HttpResponse(data)
	else:
		return render(request,'404.html',{})

def notification_view(request,id):
	profile=notification.objects.get(receiver=request.user,n_id=id)
	profile.viewed=True
	print request.GET.get('time')
	profile.save()
	if(profile.title=='Registered'):
		return HttpResponse("prfile form")
	else:
		if profile.link=='#':
			return redirect(request.GET.get('next'))
		print profile.viewed
		return HttpResponse(request.GET.get(next))

def message_view(request,dynamic_view_url):
	profile=notification.objects.get(receiver_id=dynamic_view_url)
	profile.viewed=True
	print profile.viewed
	profile.save()
	print profile.viewed
	return HttpResponse("sucess")

def all_notification(request):
	print request.user
	#profile=notification.objects.all(receiver=request.user)
	return HttpResponse('profile')

