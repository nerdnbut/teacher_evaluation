from django.urls import path
from . import views


urlpatterns = [
    path('',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.user_logout,name='logout'),
    path("student_home/",views.StudentHome,name='student_home'),
    path("teacher_home/",views.TeacherHome,name='teacher_home'),
    path("teacher/view/profile/",views.view_teacher_profile,name='view_teacher_profile'),
    path("teacher/edit/profile/",views.edit_teacher_profile,name="edit_teacher_profile"),
    path("teacher/view/student/",views.teacher_view_student,name="teacher_view_student"),

    path("teacher/edit/student/",views.teacher_edit_student,name="teacher_edit_student"),
    path("teacher/do_edit_grade/",views.teacher_do_edit_grade,name="teacher_do_edit_grade"),
    path("teacher/do_edit_evaluation/",views.teacher_do_edit_evaluation,name="teacher_do_edit_evaluation"),

    path("teacher/view/score/",views.teacher_view_score,name="teacher_view_score"),
    path("teacher/view/analysis/",views.teacher_view_analysis,name="teacher_view_analysis"),
    path("teacher/do_change_password/",views.teacher_change_password,name="teacher_change_password"),
    path("teacher/do_change_email/",views.teacher_change_email,name="teacher_change_email"),



    path("student/view/profile/",views.student_view_profile,name="view_student_profile"),
    path("student/edit/profile/",views.student_edit_profile,name="edit_student_profile"),
    path("student/do_change_password/", views.student_change_password, name="student_change_password"),
    path("student/do_change_email/", views.student_change_email, name="student_change_email"),
    path("student/evaluate_teacher/",views.student_evaluate_teacher,name="student_evaluate_teacher"),
    path("student/view/grade/",views.student_view_grade,name="student_view_grade"),
    path("student/view/analysis/",views.student_view_analysis,name="student_view_analysis"),
    path("student/do_evaluate/",views.student_do_evaluate,name="student_do_evaluate"),

    #manger管理学生
    path("manager_home/",views.manager_home,name="manager_home"),
    path("manager/view/profile/",views.manager_view_profile,name="view_manager_profile"),
    path("manager/edit/profile/",views.manager_edit_profile,name="manager_edit_profile"),
    path("manager/view/student/",views.manager_view_student,name="manager_view_student"),
    path("manager/edit/student/username/",views.manager_edit_student_username,name="manager_edit_student_username"),
    path("manager/edit/student/email/", views.manager_edit_student_email, name="manager_edit_student_email"),
    path("manager/view/teacher/",views.manager_view_teacher,name="manager_view_teacher"),
    path("manager/edit/teacher/username/",views.manager_edit_teacher_username,name="manager_edit_teacher_username"),
    path("manager/edit/teacher/email/", views.manager_edit_teacher_email, name="manager_edit_teacher_email"),
    path("manager/change/password/",views.manager_change_password,name="manager_change_password"),
    path("manager/change/email/",views.manager_change_email,name="manager_change_email"),
    path("manager/delete/student/<int:student_id>",views.manager_delete_student,name="manager_delete_student"),
    path("manager/delete/teacher/<int:teacher_id>",views.manager_delete_teacher,name="manager_delete_teacher"),

    path("reset_password/",views.reset_password.as_view(),name="reset_password")



]