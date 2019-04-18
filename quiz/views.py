from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from quiz.models import quiz_spec, question, result
from django.contrib.auth.decorators import login_required
import datetime
from student.models import Course, faculty_profile
import json
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q


# Create your views here.
@login_required
def quiz(request):
    return render(request, 'course.html', {'course': None})


@login_required
def edit_spec(request):
    course1 = Course.objects.filter(facultyassociated=request.user.faculty_profile)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        addedBy = faculty_profile.objects.get(user=request.user)
        course = Course.objects.get(course_name=request.POST.get('course', ''))
        try:
            totaltime = int(request.POST.get('time', '').strip())
        except:
            totaltime = 0
        start_date = datetime.datetime.strptime(request.POST.get('start_date', ''), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(request.POST.get('end_date', ''), '%Y-%m-%d')
        credit = int(request.POST.get('credits', '').strip())
        no_Questions = int(request.POST.get('no_Questions', '').strip())

        quiz = quiz_spec.objects.create(title=title, addedBy=addedBy, course=course, no_Questions=no_Questions,
                                        start_date=start_date, end_date=end_date, duration=totaltime, credit=credit)
        # session for quiz id
        request.session['quiz_id'] = quiz.qid

        return redirect('attach_question')
    return render(request, 'edit_spec.html', {'course': course1})


@login_required
def quiz_control(request):
    if request.session['type'] == 'faculty':
        return render(request, 'quiz_control.html')
    else:
        raise PermissionDenied()


@login_required
@csrf_exempt
def add_question(request):
    if request.method == 'POST':
        statement = request.POST.get('statement', '')
        option_A = request.POST.get('option_A', '')
        option_B = request.POST.get('option_B', '')
        option_C = request.POST.get('option_C', '')
        option_D = request.POST.get('option_D', '')
        answer = request.POST.get('answer', '')
        category = request.POST.get('category', '')
        extra_info = request.POST.get('extra_info', '')
        msg = validation_field(request)
        print request.user
        addedBy = faculty_profile.objects.get(user=request.user)
        print addedBy.user.username

        # for save and continue
        print answer

        if 'save_continue' in request.POST:
            if msg == '':
                try:
                    question.objects.create(statement=statement, a=option_A, b=option_B, c=option_C, d=option_D,
                                            addedBY=addedBy, ans=answer, category=category, extra_info=extra_info)
                except Exception as qu:
                    print qu
                return render(request, 'add_question.html', {'msg': msg})
            else:
                return render(request, 'add_question.html', {'msg': msg})
        if 'save_exit' in request.POST:
            if msg == '':
                try:
                    question.objects.create(statement=statement, a=option_A, b=option_B, c=option_C, d=option_D,
                                            addedBY=addedBy, ans=answer, category=category, extra_info=extra_info)
                except Exception as qu:
                    print qu
                if 'quiz_id' not in request.session:
                    return redirect('dashboard')
                else:
                    return redirect('attach_question')
            else:
                return redirect('dashboard')
    else:
        return render(request, 'add_question.html')


@login_required
def attach_question(request):
    if 'quiz_id' in request.session:
        quiz = quiz_spec.objects.get(qid=request.session['quiz_id'])
        q = quiz.question_set.all()
        text = request.POST.get('q_search', '')
        if text:
            qset = (
                Q(statement__icontains=text)
            )
            ques = question.objects.filter(qset).distinct()
        elif request.method == 'POST':
            category = request.POST.get('category', '')
            if category == "added":
                ques = question.objects.filter(quizes=quiz).order_by('-id')
            elif category == 'my':
                ques = question.objects.filter(addedBY=request.user.faculty_profile).order_by('-id')
            else:
                ques = question.objects.filter(category=category).order_by('-id')
        else:
            flag = request.GET.get('id', '')
            if flag == 'true':
                ques = question.objects.filter(quizes=quiz).order_by('-id')
            else:
                ques = question.objects.filter(addedBY=request.user.faculty_profile).order_by('-id')

        return render(request, 'attach_question.html', {'questions': ques, 'quiz': quiz, 'q': q})
    else:
        return HttpResponse("permission Denied")


@login_required
def quiz_confirm(request):
    if 'quiz_id' in request.session:
        quiz = quiz_spec.objects.get(qid=request.session['quiz_id'])
        try:
            q = quiz.question_set.all()
        except Exception as e:
            print e
        return render(request, 'quiz_confirm.html', {'q': q, 'quiz': quiz})
    else:
        return HttpResponse("page 404")


@login_required
def validation_field(request):
    statement = request.POST.get('statement', '')
    option_A = request.POST.get('option_A', '')
    option_B = request.POST.get('option_B', '')
    option_C = request.POST.get('option_C', '')
    option_D = request.POST.get('option_D', '')
    answer = request.POST.get('answer', '')
    category = request.POST.get('category', '')
    extra_info = request.POST.get('extra_info', '')
    msg = ''
    if statement == '':
        msg = "Enter statement"
    elif option_A == '':
        msg = 'Enter option A'
    elif option_B == '':
        msg = 'Enter option B'
    elif option_C == '':
        msg = 'Enter option C'
    elif option_D == '':
        msg = 'Enter option D'
    elif answer == '':
        msg = 'Enter answer'
    return msg


@login_required
def addquestion(request):
    print request.session['quiz_id']
    data = {}
    ques_id = (request.GET.get('id', '').strip())
    print ques_id
    quiz = quiz_spec.objects.get(qid=request.session['quiz_id'])
    ques = question.objects.get(id=ques_id)
    q = quiz.question_set.all()
    ques.quizes.add(quiz)
    ques.save()
    ques = question.objects.filter(id=ques_id)
    ques = serializers.serialize('json', ques)
    data['ques'] = ques
    data['quiz_id'] = request.session['quiz_id']
    data = json.dumps(data)
    return HttpResponse(data)


@login_required
def view_fullquestion(request):
    print "full"
    ques_id = (request.GET.get('id', '').strip())
    ques = question.objects.filter(id=ques_id)
    ques = serializers.serialize("json", ques)
    return HttpResponse(ques)


@login_required
def removeQuestion(request):
    print request.session['quiz_id']
    data = {}
    ques_id = (request.GET.get('id', '').strip())
    print ques_id
    quiz = quiz_spec.objects.get(qid=request.session['quiz_id'])
    ques = question.objects.get(id=ques_id)
    ques.quizes.remove(quiz)
    ques.save()
    ques = question.objects.filter(id=ques_id)
    ques = serializers.serialize('json', ques)
    data['ques'] = ques
    data['quiz_id'] = request.session['quiz_id']
    data = json.dumps(data)
    return HttpResponse(data)


@login_required
def qizquestions(request):
    print "inside all quiz"
    if 'id' in request.session:
        quiz = quiz_spec.objects.get(qid=request.session['id'])
    elif 'quiz_id' in request.session:
        quiz = quiz_spec.objects.get(qid=request.session['quiz_id'])
    print quiz
    try:
        q = quiz.question_set.all().order_by('?')[:quiz.no_Questions]
    except Exception as e:
        print e
    print q
    questions = serializers.serialize('json', q)
    return HttpResponse(questions)


@login_required
def EditQuiz(request):
    quizes = quiz_spec.objects.filter(addedBy=request.user.faculty_profile)
    course1 = Course.objects.filter(facultyassociated=request.user.faculty_profile)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title == '':
            return render(request, 'EditQuiz.html', {'quizes': quizes, 'courses': course1, 'msg': 'please select quiz'})
        course = Course.objects.get(course_name=request.POST.get('course', ''))
        try:
            totaltime = int(request.POST.get('time', '').strip())
        except:
            totaltime = 0
        start_date = datetime.datetime.strptime(request.POST.get('start_date', ''), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(request.POST.get('end_date', ''), '%Y-%m-%d')
        credit = int(request.POST.get('credits', '').strip())
        no_Questions = int(request.POST.get('no_Questions', '').strip())
        quiz = quiz_spec.objects.get(title=title)
        quiz.course = course
        quiz.start_date = start_date
        quiz.end_date = end_date
        quiz.duration = totaltime
        quiz.credit = credit
        quiz.no_Questions = no_Questions
        quiz.save()
        request.session['quiz_id'] = quiz.qid
        return redirect('quiz_confirm')

    return render(request, 'EditQuiz.html', {'quizes': quizes, 'courses': course1, 'msg': ''})


@login_required
def changeQuiz(request):
    data = {}
    title = request.GET.get("id")
    quiz = quiz_spec.objects.filter(title=title)
    data['course'] = quiz[0].course.course_name
    data['quiz'] = serializers.serialize('json', quiz)
    data = json.dumps(data)
    return HttpResponse(data)


@login_required
def exit(request):
    print "hello"
    quiz = quiz_spec.objects.get(qid=request.session['quiz_id'])
    questions = quiz.question_set.all()

    print  questions
    if questions.count() < quiz.no_Questions:
        return render(request, 'quiz_confirm.html',
                      {'q': questions, 'quiz': quiz, 'msg': 'Please add minimum number of Questions'})
    elif 'quiz_id' in request.session:
        del request.session['quiz_id']
        return redirect('dashboard')
    else:
        return HttpResponse("permission Denied")


@login_required
def create_course_quiz(request, id=None):
    course1 = Course.objects.filter(course_id=id)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        addedBy = faculty_profile.objects.get(user=request.user)
        course = Course.objects.get(course_name=request.POST.get('course', ''))
        try:
            totaltime = int(request.POST.get('time', '').strip())
        except:
            totaltime = 0
        start_date = datetime.datetime.strptime(request.POST.get('start_date', ''), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(request.POST.get('end_date', ''), '%Y-%m-%d')
        credit = int(request.POST.get('credits', '').strip())
        no_Questions = int(request.POST.get('no_Questions', '').strip())

        quiz = quiz_spec.objects.create(title=title, addedBy=addedBy, course=course, no_Questions=no_Questions,
                                        start_date=start_date, end_date=end_date, duration=totaltime, credit=credit)
        # session for quiz id
        request.session['quiz_id'] = quiz.qid

        return redirect('attach_question')
    return render(request, 'edit_spec.html', {'course': course1})


# stdent quiz views
@login_required
def course_quiz(request, id=None):
    course = Course.objects.filter(course_id=id)
    quiz = quiz_spec.objects.filter(course=course)
    print quiz
    return render(request, "student_quiz/course_quiz.html", {'quizes': quiz})


@login_required
def quiz_view(request, course_id, quiz_id):
    quiz = quiz_spec.objects.filter(qid=quiz_id)
    request.session['id'] = quiz_id
    return render(request, 'student_quiz/quiz_confiramation.html', {})


@login_required
def quiz_questions(request):
    if 'id' in request.session:
        quiz = quiz_spec.objects.get(qid=request.session['id'])
        if (result.objects.filter(quiz=quiz, user=request.user.student_profile).exists()):
            return render(request, "repeatquiz.html")
        else:
            result.objects.create(user=request.user.student_profile, score=0, course=quiz.course, quiz=quiz)
        questions = quiz.question_set.all()
        return render(request, 'student_quiz/quiz_question.html', {'quiz': quiz})


@login_required
def submit(request):
    return HttpResponse("sucess")


@login_required
def quiz_result(request):
    quiz = quiz_spec.objects.get(qid=request.session['id'])
    questions = quiz.question_set.all()
    print questions
    result1 = 0
    for question in questions:
        if question.ans == request.GET.get(question.statement, ''):
            result1 = result1 + 1
    print result
    st_result = result.objects.get(quiz=quiz, user=request.user.student_profile)
    st_result.score = result1
    st_result.save()
    return HttpResponse("sucess")


@login_required
def show_result(request, course):
    if request.session['type'] == 'faculty':
        course = Course.objects.get(course_id=course)
        quizes = quiz_spec.objects.filter(course=course)
        temp = 'base/sidebarf.html'
        if request.method == 'POST':
            try:
                print request.POST.get('selected_quiz')
                quiz_id = int(request.POST.get('selected_quiz'))
            except Exception as e:
                return HttpResponse(e)
            selected_quiz = quiz_spec.objects.get(qid=int(quiz_id))
            results = result.objects.filter(quiz=selected_quiz).order_by('-score')
            total = selected_quiz.no_Questions * selected_quiz.credit
            return render(request, 'quiz_result.html',
                          {'temp': temp, 'quizes': quizes, 'results': results, 'selected_quiz': selected_quiz,
                           'total': total})

        else:
            return render(request, 'quiz_result.html', {'temp': temp, 'quizes': quizes})
    else:
        return HttpResponse
    '''if request.method == 'POST':
        if 'search' in request.POST:
            quiz_id = request.POST.get('quiz')
            selected_quiz = quiz_spec.objects.get(id=quiz_id)
            results = result.objects.filter(course=selected_course,quiz=selected_quiz).order_by('-score')
            return render(request,'quiz_result.html',{'temp':temp,'quizes':quizes,'results':results,'selected_quiz':selected_quiz})

    else:
        return render(request,'quiz_result.html',{'temp':temp,'quizes':quizes})'''
