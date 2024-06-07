'''
from django.urls import path
from .views import teacher_home, student_home, student_conversations, teacher_conversations, conversation_detail, send_message

urlpatterns = [
    path('teacher/home/', teacher_home, name='teacher_home'),
    path('student/home/', student_home, name='student_home'),
    path('student/conversations/<int:teacher_id>/', student_conversations, name='student_conversations'),
    path('teacher/conversations/<int:student_id>/', teacher_conversations, name='teacher_conversations'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('send_message/<int:conversation_id>/', send_message, name='send_message'),

]
'''
from django.urls import path
from . import views

urlpatterns = [
    path('teacher/students/<int:course_id>/', views.teacher_students, name='teacher_students'),
    path('student/teachers/<int:course_id>/', views.student_teachers, name='student_teachers'),
    path('teacher/conversations/<int:student_id>/', views.teacher_conversations, name='teacher_conversations'),
    path('student/conversations/<int:teacher_id>/', views.student_conversations, name='student_conversations'),
]
