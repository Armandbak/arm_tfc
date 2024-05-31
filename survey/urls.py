from django.contrib.auth.views import LoginView
from django.urls import path

from survey import views

urlpatterns = [
    path('adminlogin', LoginView.as_view(template_name='survey/login.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('add_course/', views.add_course_view, name='add_course'),
    path('course_success/', views.course_success_view, name='course_success'),
    path('add_question/', views.add_question_view, name='add_question'),
    path('question_success/', views.question_success_view, name='question_success'),
    path('courses/', views.course_list, name='course_list'),
    path('courses-teacher/', views.course_list_adm, name='course_list_teacher'),
    path('courses-list/', views.course_list_total, name='course_list_total'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses_student/<int:course_id>/', views.course_detail_student, name='course_detail_student'),
    path('courses_eval/<int:course_id>/', views.course_Eval, name='course_student_eval'),
    path('courses/<int:course_id>/inscrire/', views.inscrire, name='inscrire'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_course, name='delete_question'),
    path('admin-view-student', views.student_list,name='student_list'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('add_question_eee/', views.add_question_eee, name='question_eee'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,name='admin-view-pending-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),

]