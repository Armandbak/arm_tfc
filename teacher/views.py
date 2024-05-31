from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from survey import models as QMODEL
from student import models as SMODEL

def teacher_signup_view(request):
    userForm = forms.TeacherUserForm()
    teacherForm = forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method=='POST':
        userForm = forms.TeacherUserForm(request.POST)
        teacherForm = forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'survey/teacher/register_teacher.html',context=mydict)


@login_required
def teacher_dashboard_view(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'total_student': SMODEL.Student.objects.all().count(),
        'active_link': 'dashboard'
    }
    return render(request, 'survey/teacher/dashboardteacher.html', context=dict)

@login_required
def check_marks(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    results = QMODEL.Result.objects.all().filter(exam=course).filter(soumis=True)
    return render(request, 'survey/teacher/mark.html', {'results': results})

