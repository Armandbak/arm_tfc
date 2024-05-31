
# views.py dans votre application de messagerie (par exemple, 'messaging')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from student.models import Student
from teacher.models import Teacher
from .models import Conversation, ConversationUser, Message

@login_required
def teacher_conversations(request, student_id):
    students_ifd = Student.objects.all()
    student = Student.objects.get(user_id=student_id)
    conversation = Conversation.objects.filter(conversationuser__user=request.user, conversationuser__conversation__conversationuser__user=student.user).first()
    if conversation is None:
        # Si la conversation n'existe pas, créez-en une nouvelle
        conversation = Conversation.objects.create()
        ConversationUser.objects.create(user=request.user, conversation=conversation)
        ConversationUser.objects.create(user=student.user, conversation=conversation)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(from_user=request.user, conversation=conversation, content=content)
        return redirect('teacher_conversations', student_id=student_id)
    messages = Message.objects.filter(conversation=conversation)
    return render(request, 'messagerie/teacher_conversation.html', {'student': student, 'messages': messages, 'students_ifd': students_ifd})

@login_required
def student_conversations(request, teacher_id):
    teachers_ifn = Teacher.objects.filter(status=True)
    student_conn = request.user
    teacher = Teacher.objects.get(user_id=teacher_id)
    conversation = Conversation.objects.filter(conversationuser__user=request.user, conversationuser__conversation__conversationuser__user=teacher.user).first()
    if conversation is None:
        # Si la conversation n'existe pas, créez-en une nouvelle
        conversation = Conversation.objects.create()
        ConversationUser.objects.create(user=request.user, conversation=conversation)
        ConversationUser.objects.create(user=teacher.user, conversation=conversation)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(from_user=request.user, conversation=conversation, content=content)
        return redirect('student_conversations', teacher_id=teacher_id)
    messages = Message.objects.filter(conversation=conversation)
    return render(request, 'messagerie/student_conversation.html', {'teacher': teacher, 'messages': messages, 'student_conn': student_conn, 'teachers_ifn': teachers_ifn})


@login_required
def teacher_students(request):
    students = Student.objects.all()
    return render(request, 'messagerie/teacher_students.html', {'students': students, 'active_link': 'message'})

@login_required
def student_teachers(request):
    teachers = Teacher.objects.filter(status=True)
    return render(request, 'messagerie/student_teachers.html', {'teachers': teachers, 'active_link': 'message'})


