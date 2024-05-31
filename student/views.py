from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from survey.models import Course, Inscription
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from survey import models as SMODEL
from .models import Student
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden


def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'survey/student/register_student.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict = {
        'total_course': SMODEL.Course.objects.all().count(),
        'total_question': SMODEL.Question.objects.all().count(),
        #'tota_question_inscrit':Inscription.objects.filter(etudiant=request.user).count(),
        'active_link': 'dashboard',
    }
    return render(request, 'survey/student/dashboardstudent.html', context=dict)


from django.contrib.auth.decorators import login_required



@login_required
def inscrire(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    try:
        student_profile = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponseForbidden("Vous devez être un étudiant pour vous inscrire à ce cours.")

    if request.method == 'POST':
        Inscription.objects.create(cours=course, etudiant=student_profile)
        return redirect('course_detail', course_id=course_id)

    return render(request, 'inscrire.html', {'course': course})

@login_required
def enrolled_courses(request):
    try:
        student_profile = Student.objects.get(user=request.user)
        active_link = 'result'
    except Student.DoesNotExist:
        return HttpResponseForbidden("Vous devez être un étudiant pour voir vos cours inscrits.")

    inscriptions = Inscription.objects.filter(etudiant=student_profile)
    courses = [inscription.cours for inscription in inscriptions]
    return render(request, 'survey/student/enrolled_courses.html', {'courses': courses, 'active_link': active_link})


@login_required
def calculate_marks(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        if course_id:
            try:
                course = SMODEL.Course.objects.get(id=course_id)
                total_marks = 0
                questions = SMODEL.Question.objects.filter(course=course)

                for question in questions:
                    selected_ans = request.POST.get(f'question_{question.id}')
                    if selected_ans and selected_ans == question.response:
                        total_marks += question.marks

                student = models.Student.objects.get(user_id=request.user.id)
                result, created = SMODEL.Result.objects.update_or_create(
                    student=student,
                    exam=course,
                    defaults={'marks': total_marks, 'soumis': True}
                )

                if not created:
                    result.soumis = False
                    result.save()

                return redirect('course_list_total')

            except SMODEL.Course.DoesNotExist:
                # Handle the case where the course does not exist
                pass

            except IntegrityError:
                # Handle the case where there is an integrity error
                pass

    return redirect('course_list_total')

@login_required
def check_marks_view(request,pk):
    course = SMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = SMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'survey/student/mark.html', {'results':results})

