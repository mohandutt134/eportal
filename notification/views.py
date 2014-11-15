from django.shortcuts import render

#imported from student.views im imports

import uuid
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, render, redirect
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
from .utils import slug2id

# Create your views here.
@login_required
def all(request):
    """
    Index page for authenticated user
    """
    return render(request, 'notifications/list.html', {
        'notifications': request.user.notifications.all()
    })
    actions = request.user.notifications.all()

    paginator = Paginator(actions, 16) # Show 16 notifications per page
    page = request.GET.get('p')

    try:
        action_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        action_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        action_list = paginator.page(paginator.num_pages)

    return render_to_response('notifications/list.html', {
        'member': request.user,
        'action_list': action_list,
    }, context_instance=RequestContext(request))

@login_required
def unread(request):
    return render(request, 'notifications/list.html', {
        'notifications': request.user.notifications.unread()
    })

@login_required
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)
    return redirect('notifications:all')

@login_required
def mark_as_read(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_read()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')

@login_required
def mark_as_unread(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_unread()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')

@login_required
def delete(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.delete()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')