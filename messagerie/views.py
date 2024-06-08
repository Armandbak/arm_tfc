
# views.py dans votre application de messagerie (par exemple, 'messaging')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from student.models import Student
from survey.models import Ec, Inscription
from teacher.models import Teacher
from .models import Conversation, ConversationUser, Message

@login_required
def teacher_conversations(request, student_id):
    teacher = Teacher.objects.get(user=request.user)
    courses = Ec.objects.filter(teacher=teacher)
   # students_ifd = Student.objects.all()
    inscriptions = Inscription.objects.filter(cours__in=courses)
    students_ifd = Student.objects.filter(inscriptions__in=inscriptions).distinct()
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
   # teachers_ifn = Teacher.objects.filter(status=True)
    student = Student.objects.get(user=request.user)

    # Obtenir les inscriptions de l'étudiant connecté
    inscriptions = Inscription.objects.filter(etudiant=student)

    # Obtenir les cours auxquels l'étudiant est inscrit
    courses = inscriptions.values_list('cours', flat=True)

    # Obtenir les enseignants de ces cours
    teachers_ifn = Teacher.objects.filter(
        id__in=Ec.objects.filter(id__in=courses).values_list('teacher_id', flat=True)).distinct()

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

def teacher_students(request, course_id=None):
    # Assurez-vous que l'utilisateur connecté est un enseignant
    teacher = Teacher.objects.get(user=request.user)

    if course_id:
        # Si un ID de cours est fourni, filtrer les étudiants pour ce cours spécifique
        course = get_object_or_404(Ec, pk=course_id)
        students = course.inscriptions.all().values_list('etudiant', flat=True)
        students = Student.objects.filter(id__in=students).distinct()
    else:
        # Sinon, obtenir tous les étudiants des cours enseignés par l'enseignant connecté
        courses = Ec.objects.filter(teacher=teacher)
        inscriptions = Inscription.objects.filter(cours__in=courses)
        students = Student.objects.filter(inscriptions__in=inscriptions).distinct()

    return render(request, 'messagerie/teacher_students.html', {'students': students, 'active_link': 'message'})

@login_required
def student_teachers(request, course_id=None):
    # Assurez-vous que l'utilisateur connecté est un étudiant
    student = Student.objects.get(user=request.user)

    # Obtenir les inscriptions de l'étudiant connecté
    inscriptions = Inscription.objects.filter(etudiant=student)

    if course_id:
        # Si un ID de cours est fourni, filtrer les enseignants pour ce cours spécifique
        course = get_object_or_404(Ec, pk=course_id)
        teachers = course.teacher
    else:
        # Sinon, obtenir tous les enseignants des cours auxquels l'étudiant est inscrit
        courses = inscriptions.values_list('cours', flat=True)
        teachers = Teacher.objects.filter(id__in=Ec.objects.filter(id__in=courses).values_list('teacher_id', flat=True)).distinct()

    return render(request, 'messagerie/student_teachers.html', {'teachers': teachers, 'active_link': 'message'})


