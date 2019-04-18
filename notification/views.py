from django.http import HttpResponse
from student.models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect
from notification.models import notification, message
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied


@csrf_exempt
def notification_create(request):
    if request.method == 'POST':
        data = {}
        data['notifications'] = serializers.serialize("json",
                                                      notification.objects.filter(receiver=request.user, viewed=False))
        data['messages'] = serializers.serialize("json", message.objects.filter(receiver=request.user, viewed=False))
        data = json.dumps(data)
        return HttpResponse(data)
    else:
        raise PermissionDenied


def notification_view(request, id):
    profile = notification.objects.get(receiver=request.user, pk=id)
    profile.viewed = True
    profile.save()
    if profile.link == '#':
        return redirect(request.GET.get('next'))
    return redirect(profile.link)


@csrf_exempt
def message_view(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        msg = message.objects.get(m_id=id, receiver=request.user)
        msg.viewed = True
        msg.save()
        msg = message.objects.filter(m_id=id, receiver=request.user)
        data = serializers.serialize("json", msg)
        return HttpResponse(data)
    else:
        raise PermissionDenied


def all_notification(request):
    print request.user
    # profile=notification.objects.all(receiver=request.user)
    return HttpResponse('profile')


def bulk_message(request, id):
    if request.method == 'POST':
        try:
            course = Course.objects.get(course_id=id, facultyassociated=request.user.faculty_profile)
            receivers = student_profile.objects.filter(coursetaken=course)
            print receivers
            for receiver in receivers:
                message.objects.create(title=request.POST.get('title'), body=request.POST.get('body'),
                                       sender=request.user, senderName=request.user.first_name,
                                       senderImage=request.user.faculty_profile.image, receiver=receiver.user)
            message.objects.create(title="Delivery Report", body="Your message has been delivered successfully",
                                   sender=User.objects.get(username="admin"), receiver=request.user)
            return redirect(request.GET.get('next'))
        except Exception as e:
            return HttpResponse(e)
    else:
        raise PermissionDenied


@csrf_exempt
def messageToFaculty(request, email):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            body = request.POST.get('body')
            receiver = User.objects.get(email=email)
            if request.session['type'] == 'faculty':
                message.objects.create(title=title, body=body, sender=request.user, senderName=request.user.first_name,
                                       senderImage=request.user.faculty_profile.image, receiver=receiver)
            else:
                message.objects.create(title=title, body=body, sender=request.user, senderName=request.user.first_name,
                                       senderImage=request.user.student_profile.image, receiver=receiver)
            return HttpResponse("success")
        except Exception as e:
            return HttpResponse("success")
    else:
        raise PermissionDenied
