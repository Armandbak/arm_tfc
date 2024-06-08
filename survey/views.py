import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from student.models import Student
from teacher.models import Teacher
from .forms import CourseForm, UenseignementForm
#from .forms import UserForm, StudentProfileForm, TeacherProfileForm
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from . import forms,models
from survey import forms as QFORM
from .models import Question, Ec, Inscription, Result, Uenseignement
from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Question
import json



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'survey/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_student(request.user):
        return redirect('student/student-dashboard')

    elif is_teacher(request.user):
        accountapproval = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request, 'survey/index.html')
    else:
        return redirect('admin-dashboard')

@login_required
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Ec.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
    'active_link': 'dashboard',
    }
    return render(request,'survey/dashboard.html',context=dict)

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_success')  # Redirige vers une page de succès après l'ajout du cours
    else:
        form = CourseForm()

    return render(request, 'survey/add_course.html', {'form': form})

@login_required
def add_course_view(request):
    try:
        teacher_profile = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher_profile
            course.save()
            return redirect('course_list')  # Redirigez vers une vue appropriée après l'ajout du cours
    else:
        form = CourseForm()
    return render(request, 'survey/add_course.html', {'form': form})

@login_required(login_url='adminlogin')
def add_ue_view(request):

    if request.method == 'POST':
        form = UenseignementForm(request.POST)
        if form.is_valid():
            ue = form.save(commit=False)
            ue.save()
            return redirect('ue_list')  # Redirigez vers une vue appropriée après l'ajout du cours
    else:
        form = CourseForm()
    return render(request, 'survey/add_ue.html', {'form': form})
@login_required
def course_success_view(request):
    return render(request, 'survey/course_success.html')

@login_required
def add_question_view(request):
    active_link = 'question'
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Traiter les options comme JSON
            options = request.POST.getlist('options')
            options_json = json.dumps(options)
            question = form.save(commit=False)
            question.options = options_json
            question.save()
            return redirect('course_list')
    else:
        form = QuestionForm()

    return render(request, 'survey/add_question.html', {'form': form, 'active_link': active_link})

@login_required
def add_question_eee(request):
    active_link = 'question'
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Traiter les options comme JSON
            options = request.POST.getlist('options')
            options_json = json.dumps(options)
            question = form.save(commit=False)
            question.options = options_json
            question.save()
            return redirect('question_success')
    else:
        form = QuestionForm()

    return render(request, 'survey/question_eee.html', {'form': form, 'active_link': active_link})

@login_required
def question_success_view(request):
    return render(request, 'survey/question_success.html')

@login_required
def course_list(request):
    courses = Ec.objects.all()
    active_link = 'course'
    return render(request, 'survey/course_list.html', {'courses': courses, 'active_link': active_link})

@login_required
def ue_list(request):
    ue = Uenseignement.objects.all()
    active_link = 'course'
    return render(request, 'survey/ue_list.html', {'ues': ue, 'active_link': active_link})



def ec_list(request):
    courses = Ec.objects.all()
    active_link = 'course'
    return render(request, 'messagerie/ec_list.html', {'courses': courses, 'active_link': active_link})
def ec_student_list(request):
    courses = Ec.objects.all()
    active_link = 'course'
    return render(request, 'messagerie/ec_student_list.html', {'courses': courses, 'active_link': active_link})

@login_required
def course_list_adm(request):
    ue = Ec.objects.all()
    active_link = 'course'
    return render(request, 'survey/course_list_adm.html', {'ue': ue, 'active_link': active_link})

@login_required
def course_list_total(request):
    courses = Ec.objects.all()
    active_link = 'course'
    return render(request, 'survey/course_list_total.html', {'courses': courses, 'active_link': active_link})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Ec, pk=course_id)
    questions = Question.objects.filter(course=course)
    active_link = 'course'

    for question in questions:
        question.options_list = question.options.split(',')
    return render(request, 'survey/course_detail.html', {'course': course, 'questions': questions, 'active_link': active_link})

@login_required
def course_detail_student(request, course_id):
    course = get_object_or_404(Ec, pk=course_id)
    questions = Question.objects.filter(course=course)
    active_link = 'course'

    for question in questions:
        question.options_list = question.options.split(',')
    return render(request, 'survey/detail_student.html', {'course': course, 'questions': questions, 'active_link': active_link})

@login_required
def course_Eval(request, course_id):
    course = get_object_or_404(Ec, pk=course_id)
    questions = Question.objects.filter(course=course)
    active_link = 'evaluation'

    student = models.Student.objects.get(user_id=request.user.id)
    result = Result.objects.filter(student=student, exam=course).first()

    already_submitted = result.soumis if result else False

    response = render(request, 'survey/student/evaluation.html', {
        'course': course,
        'questions': questions,
        'active_link': active_link,
        'already_submitted': already_submitted
    })

    response.set_cookie('course_id', course.id)
    return response

@login_required
@user_passes_test(is_student)
def inscrire(request, course_id):
    course = get_object_or_404(Ec, id=course_id)
    try:
        student_profile = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponseForbidden("Vous devez être un étudiant pour vous inscrire à ce cours.")


    Inscription.objects.create(cours=course, etudiant=student_profile)
    return redirect('enrolled_courses')



@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Ec, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'survey/teacher/edit_course.html', {'form': form})


@login_required
def edit_ue(request, ue_id):
    ue = get_object_or_404(Uenseignement, id=ue_id)
    if request.method == 'POST':
        form = UenseignementForm(request.POST, instance=ue)
        if form.is_valid():
            form.save()
            return redirect('ue_list')
    else:
        form = UenseignementForm(instance=ue)
    return render(request, 'survey/update_ue.html', {'form': form})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Ec, id=course_id)
    course.delete()
    return redirect('course_list')

@login_required
def delete_ue(request, ue_id):
    ue = get_object_or_404(Uenseignement, id=ue_id)
    ue.delete()
    return redirect('ue_list')


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            options = request.POST.getlist('options')
            options_json = json.dumps(options)
            questions = form.save(commit=False)
            questions.options = options_json
            form.save()
            return redirect('course_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'survey/teacher/edit_question.html', {'form': form})

#def delete_course(request, question_id):
 #   question = get_object_or_404(Question, id=question_id)
  #  question.delete()
   # return redirect('course_detail')


@login_required
def student_list(request):
    students= SMODEL.Student.objects.all()
    active_link = 'student'
    return render(request,'survey/student_list.html',{'students':students, 'active_link': active_link})


@login_required
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'survey/update_student.html', context=mydict)



@login_required
def delete_student_view(request,pk):
    student = SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')

@login_required
def approve_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect('admin-view-teacher')


@login_required
def admin_view_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    active_link = 'teacher'
    return render(request,'survey/teacher_list.html',{'teachers':teachers, 'active_link': active_link})


@login_required
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'survey/modif_teacher.html',context=mydict)



@login_required
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    active_link = 'teacher'
    return render(request,'survey/non_inscrit.html',{'teachers':teachers, 'active_link': active_link})

@login_required
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')