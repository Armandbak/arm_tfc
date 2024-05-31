from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentsignup', views.student_signup_view,name='studentsignup'),
    path('studentlogin', LoginView.as_view(template_name='survey/student/loginstudent.html'),name='studentlogin'),
    path('student-dashboard', views.student_dashboard_view, name='student-dashboard'),
    path('my-courses/', views.enrolled_courses, name='enrolled_courses'),
    path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),
    path('calculate-marks', views.calculate_marks, name='calculate-marks'),

]