from django.shortcuts import render,redirect
from django.conf import settings
import os
from django.template.context import RequestContext
from quiz.models import question
from django.core.context_processors import csrf
from django.http import HttpResponse
from student.models import Course
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from quiz.models import quiz_spec,question
import datetime
from student.models import student_profile,Course,faculty_profile
import json
from django.core import serializers

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
def quiz(request):
	return render(request,'course.html',{'course':course})

def edit_spec(request):
	course1=Course.objects.filter(facultyassociated=request.user.faculty_profile)
	if request.method=='POST':
		title=request.POST.get('title','')
		course=Course.objects.get(course_name=request.POST.get('course',''))
		try:
			totaltime=int(request.POST.get('time','').strip())
		except:
			totaltime=0
		start_date=datetime.datetime.strptime(request.POST.get('start_date',''), '%Y-%m-%d')
		end_date=datetime.datetime.strptime(request.POST.get('end_date',''), '%Y-%m-%d')
		credit=int(request.POST.get('credits','').strip())
		
		quiz=quiz_spec.objects.create(title=title,course=course,start_date=start_date,end_date=end_date,duration=totaltime,credit=credit)
		#session for quiz id
		request.session['quiz_id'] =quiz.id
		
		return redirect('attach_question')
	return render(request, 'edit_spec.html',{'course':course1})




def quiz_control(request):
	return render(request, 'quiz_control.html')



@csrf_exempt
def add_question(request):
	if request.method=='POST':
		statement=request.POST.get('statement','')
		option_A=request.POST.get('option_A','')
		option_B=request.POST.get('option_B','')
		option_C=request.POST.get('option_C','')
		option_D=request.POST.get('option_D','')
		answer=request.POST.get('answer','')
		category=request.POST.get('category','')
		extra_info=request.POST.get('extra_info','')
		msg=validation_field(request)
		print request.user
		addedBy=faculty_profile.objects.get(user=request.user)
		print addedBy.user.username

		#for save and continue
		print answer
	
		if 'save_continue' in request.POST:
			if msg=='':
				try:
					question.objects.create(statement=statement,a=option_A,b=option_B,c=option_C,d=option_D,addedBY=addedBy,ans=answer,category=category,extra_info=extra_info)
				except Exception as qu:
					print qu
				return render(request, 'add_question.html',{'msg':msg})
			else:
				return render(request, 'add_question.html',{'msg':msg})
		if 'save_exit' in request.POST:
			if msg=='':
				try:
					question.objects.create(statement=statement,a=option_A,b=option_B,c=option_C,d=option_D,addedBY=addedBy,ans=answer,category=category,extra_info=extra_info)
				except Exception as qu:
					print qu
				return render(request, 'add_question.html')
	else:
		return render(request, 'add_question.html')



def attach_question(request):
	if request.method=='POST':
		category=request.POST.get('category','')
		print category
		if category=='my':
			ques=question.objects.filter(addedBY=request.user.faculty_profile)
		else:
			ques=question.objects.filter(category=category)
		return render(request, 'attach_question.html',{'questions':ques})
	else:	
		ques=question.objects.filter(addedBY=request.user.faculty_profile)
		return render(request, 'attach_question.html',{'questions':ques})



def quiz_confirm(request):
	quiz=quiz_spec.objects.get(id=request.session['quiz_id'])
	print request.session['quiz_id']
	ques=question.objects.filter(quizes=quiz)
	print quiz
	try:
		q=quiz.question_set.all()
	except Exception as e:
		print e
	print ques.count()
	return render(request, 'quiz_confirm.html',{'q':q,'quiz':quiz})



def validation_field(request):
	statement=request.POST.get('statement','')
	option_A=request.POST.get('option_A','')
	option_B=request.POST.get('option_B','')
	option_C=request.POST.get('option_C','')
	option_D=request.POST.get('option_D','')
	answer=request.POST.get('answer','')
	category=request.POST.get('category','')
	extra_info=request.POST.get('extra_info','')
	msg=''
	if statement=='':
		msg="Enter statement"
	elif option_A=='':
		msg='Enter option A'
	elif option_B=='':
		msg='Enter option B'
	elif option_C=='':
		msg='Enter option C'
	elif option_D=='':
		msg='Enter option D'
	elif answer=='':
		msg='Enter answer'
	return msg
	

def addquestion(request):
	print request.session['quiz_id']
	data={}
	ques_id=(request.GET.get('id','').strip())
	print ques_id
	quiz=quiz_spec.objects.get(id=request.session['quiz_id'])
	ques=question.objects.get(id=ques_id)
	ques.quizes.add(quiz)
	ques.save()
	ques=question.objects.filter(id=ques_id)
	ques=serializers.serialize('json',ques)
	data['ques']=ques
	data['quiz_id']=request.session['quiz_id']
	data=json.dumps(data)
	return HttpResponse(data)


def view_fullquestion(request):
	print "full"
	ques_id=(request.GET.get('id','').strip())
	ques=question.objects.filter(id=ques_id)
	ques=serializers.serialize("json",ques)
	return HttpResponse(ques)

def removeQuestion(request):
	print request.session['quiz_id']
	data={}
	ques_id=(request.GET.get('id','').strip())
	print ques_id
	quiz=quiz_spec.objects.get(id=request.session['quiz_id'])
	ques=question.objects.get(id=ques_id)
	ques.quizes.remove(quiz)
	ques.save()
	ques=question.objects.filter(id=ques_id)
	ques=serializers.serialize('json',ques)
	data['ques']=ques
	data['quiz_id']=request.session['quiz_id']
	data=json.dumps(data)
	return HttpResponse(data)


def qizquestions(request):
	print "inside all quiz"
	quiz=quiz_spec.objects.get(id=request.session['quiz_id'])
	print request.session['quiz_id']
	ques=question.objects.filter(quizes=quiz)
	print quiz
	try:
		q=quiz.question_set.all()
	except Exception as e:
		print e
	questions=serializers.serialize('json',q)
	return HttpResponse(questions)
	