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
from student.models import *
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
from notification.models import notification,message
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def notificationicon_create(request):
	if(request.method=='POST'):
		data = {}
		data['notifications']=serializers.serialize("json",notification.objects.filter(receiver=request.user,viewed=False))
		data['messages']=serializers.serialize("json",message.objects.filter(receiver=request.user,viewed=False))
		data=json.dumps(data)
		return HttpResponse(data)
	else:
		return render(request,'404.html',{})

def notification_view(request,id):
	profile=notification.objects.get(receiver=request.user,n_id=id)
	profile.viewed=True
	print request.GET.get('time')
	profile.save()
	if profile.link=='#':
		return redirect(request.GET.get('next'))
	print profile.viewed
	return redirect(profile.link)

@csrf_exempt
def message_view(request):
	if(request.method=='POST'):
		id = request.POST.get('id')
		msg = message.objects.get(m_id=id,receiver=request.user)
		msg.viewed=True
		msg.save()
		msg=message.objects.filter(m_id=id,receiver=request.user)
		data = {}
		data=serializers.serialize("json",msg)
		return HttpResponse(data)
	else:
		return render(request,'404.html',{})

def all_notification(request):
	print request.user
	#profile=notification.objects.all(receiver=request.user)
	return HttpResponse('profile')


def bulk_message(request,id):
	if request.method=='POST':
		try:
			course = Course.objects.get(course_id=id,facultyassociated=request.user.faculty_profile)
			receivers = student_profile.objects.filter(coursetaken=course)
			print receivers
			for receiver in receivers:
				message.objects.create(title=request.POST.get('title'),body=request.POST.get('body'),sender=request.user,senderName=request.user.first_name,senderImage=request.user.faculty_profile.image,receiver=receiver.user)
			message.objects.create(title="Delivery Report",body="Your message has been delivered successfully",sender=User.objects.get(username="kraken"),receiver=request.user)
			return redirect(request.GET.get('next'))
		except Exception as e:
			return HttpResponse(e)
	else:
		return HttpResponse("Permission Denied")


@csrf_exempt
def messageToFaculty(request,email):
	if request.method=='POST':
		try:
			title = request.POST.get('title')
			body = request.POST.get('body')
			receiver = User.objects.get(email=email)
			if request.user.faculty_profile:
				message.objects.create(title=title,body=body,sender=request.user,senderName=request.user.first_name,senderImage=request.user.faculty_profile.image,receiver=receiver)
			else:
				message.objects.create(title=title,body=body,sender=request.user,senderName=request.user.first_name,senderImage=request.user.student_profile.image,receiver=receiver)
			return HttpResponse("success")
		except Exception as e:
			return HttpResponse("success")
	else:
		return HttpResponse("Permission Denied")
