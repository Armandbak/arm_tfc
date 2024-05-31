from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('teachersignup', views.teacher_signup_view,name='teachersignup'),
    path('teacherlogin', LoginView.as_view(template_name='survey/teacher/loginteacher.html'), name='teacherlogin'),
    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('check-marks/<int:pk>', views.check_marks, name='check-mar'),
]