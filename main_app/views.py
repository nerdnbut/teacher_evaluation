from teacher_evaluation import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from main_app.forms import *
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main_app.forms import *
from main_app.models import *
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_type == 0:
                return redirect(reverse("student_home"))
            elif request.user.user_type == 1:
                return redirect(reverse("teacher_home"))
            else:
                return redirect(reverse("manager_home"))
        form = LoginForm()
        return render(request, 'main_template/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                messages.success(request, '登录成功!')
                login(request, user)
                if user.user_type == 0:
                    return redirect(reverse("student_home"))
                elif user.user_type == 1:
                    return redirect(reverse("teacher_home"))
                else:
                    return redirect(reverse("manager_home"))
            else:
                messages.error(request, '账号或密码错误!')
                return redirect(reverse("login"))
        else:
            messages.error(request, '账号或密码不合法!')
            return redirect(reverse("login"))


class RegisterView(View):
    def get(self, request):
        context = {
            'form': RegisterForm()
        }
        return render(request, 'main_template/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_type = int(form.cleaned_data.get('user_type'))
            username = form.cleaned_data.get('username')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = CustomUser.objects.create_user(username, email=email, password=password, user_type=user_type,
                                                  gender=gender)
            user.save()
            return redirect(reverse("login"))
        else:
            messages.error(request, '注册失败,请检查信息是否正确!')
            return redirect(reverse("register"))


def user_logout(request):
    if request.user is not None:
        logout(request)
    messages.success(request, "登出成功")
    return redirect('/')


@login_required
def StudentHome(request):
    user = request.user
    student = Student.objects.get(user=user)
    scores = StudentGrade.objects.filter(student=student)
    sum_score = 0
    count = 0
    for score in scores:
        sum_score += score.grade
        count += 1
    if count == 0:
        avg_score = 0
    else:
        avg_score = sum_score / count

    all_course = Course.objects.filter(student=student)
    total_course = all_course.count()
    course_names = [course.course_name for course in all_course]
    grades = []
    for course in all_course:
        student_grade = StudentGrade.objects.filter(student=student, course=course)
        for grade in student_grade:
            grades.append(grade.grade)

    context = {
        "user": user,
        "avg_score": avg_score,
        "total_course": total_course,

        'course_names': course_names,
        'grades': grades,
        'MEDIA_URL': settings.MEDIA_URL
    }
    return render(request, "student_template/student_home.html", context)


@login_required
def TeacherHome(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    total_student = Student.objects.all().count()
    course = get_object_or_404(Course, teacher=teacher)
    teacher = Teacher.objects.get(user=user)
    recent_score_all = TeacherGrade.objects.filter(teacher=teacher)
    all_score = 0

    like_count = 0

    for score in recent_score_all:
        all_score += score.grade
        if score.grade >= 60:
            like_count += 1

    if recent_score_all.exists():
        like_rate = round(like_count / recent_score_all.count(), 2) * 100
        average_score = round(all_score / recent_score_all.count(), 2)
    else:
        like_rate = 0
        average_score = 0
    all_student = Student.objects.filter(course=course).count()
    students = Student.objects.filter(course=course)
    student_names = [student.user.username for student in students]
    # 成绩

    student_grade_data = []
    for student in students:
        student_grade = StudentGrade.objects.filter(course=course, student=student)
        count = 0
        sum_grade = 0
        for grade in student_grade:
            sum_grade += grade.grade
            count += 1
        if sum_grade == 0:
            student_grade_data.append(sum_grade)
        student_grade_data.append(round(sum_grade / count, 2))

    context = {
        "user": user,
        "total_student": total_student,
        "course": course,
        "teacher_score": average_score,
        "like_rate": like_rate,
        'all_student': all_student,

        'student_names': student_names,
        'student_grade_data': student_grade_data,

        'MEDIA_URL': settings.MEDIA_URL

    }

    return render(request, "teacher_template/teacher_home.html", context)


def view_teacher_profile(request):
    user = request.user
    total_student = Student.objects.all().count()
    course = Course.objects.get(teacher=user.teacher)
    recent_score_all = TeacherGrade.objects.filter(teacher=user.teacher)
    all_score = 0
    all_course = 0
    for score in recent_score_all:
        all_score += score.grade
        all_course += 1
    if recent_score_all.exists():
        average_score = round(all_score / recent_score_all.count(), 2)
    else:
        average_score = 0
    context = {
        'user': request.user,
        "course": course,
        "average_score": average_score,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, "teacher_template/teacher_view_profile.html", context)


def edit_teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == "GET":
        user_form = UserForm(instance=teacher)
        change_password_form = ChangePasswordForm(request.user)
        change_email_form = ChangeEmailForm()
        context = {
            'user_form': user_form,
            "change_password_form": change_password_form,
            "change_email_form": change_email_form,
        }
        return render(request, "teacher_template/teacher_edit_profile.html", context)
    else:
        user_form = UserForm(request.POST, instance=teacher)
        if user_form.is_valid():
            username = user_form.cleaned_data.get("username")
            gender = user_form.cleaned_data.get("gender")
            self = user_form.cleaned_data.get("self")
            user = request.user
            user.username = username
            user.gender = gender
            user.self = self

            user.save()
            return redirect(reverse("edit_teacher_profile"))
        else:
            return redirect(reverse("edit_teacher_profile"))


def edit_student_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "GET":
        user_form = UserForm(instance=student)
        change_password_form = ChangePasswordForm(request.user)
        change_email_form = ChangeEmailForm()
        context = {
            'user_form': user_form,
            "change_password_form": change_password_form,
            "change_email_form": change_email_form,
        }
        return render(request, "student_template/student_edit_profile.html", context)
    else:
        user_form = UserForm(request.POST, instance=student)
        if user_form.is_valid():
            username = user_form.cleaned_data.get("username")
            gender = user_form.cleaned_data.get("gender")
            self = user_form.cleaned_data.get("self")
            user = request.user
            user.username = username
            user.gender = gender
            user.self = self

            user.save()
            return redirect(reverse("edit_student_profile"))
        else:
            return redirect(reverse("edit_student_profile"))


def teacher_change_password(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == "POST":
        password_form = ChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            new_password = password_form.cleaned_data.get("new_password1")
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "修改成功")
            return redirect(reverse("edit_teacher_profile"))
        else:
            errors = password_form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
            return redirect(reverse("edit_teacher_profile"))
    return redirect(reverse("edit_teacher_profile"), locals())


def student_change_password(request):
    if request.method == "POST":
        password_form = ChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            new_password = password_form.cleaned_data.get("new_password1")
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "修改成功")
            return redirect(reverse("edit_student_profile"))
        else:
            errors = password_form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
            return redirect(reverse("edit_student_profile"))
    return redirect(reverse("edit_student_profile"), locals())


def teacher_change_email(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get("email")
            user = request.user
            user.email = email
            user.save()
            messages.success(request, "修改成功")
            return redirect(reverse("edit_teacher_profile"))
        else:
            errors = email_form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
            return redirect(reverse("edit_teacher_profile"))
    return redirect(reverse("edit_teacher_profile"), locals())


def student_change_email(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get("email")
            user = request.user
            user.email = email
            user.save()
            messages.success(request, "修改成功")
            return redirect(reverse("edit_student_profile"))
        else:
            errors = email_form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
            return redirect(reverse("edit_student_profile"))
    return redirect(reverse("edit_student_profile_profile"), locals())


def teacher_view_student(request):
    teacher = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(course=teacher.course)
    teacher_course = teacher.course.course_name
    context = {
        "students": students,
        "teacher_course": teacher_course
    }
    return render(request, "teacher_template/teacher_view_student.html", context)


def teacher_edit_student(request):
    teacher = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(course=teacher.course)
    teacher_course = teacher.course.course_name
    context = {
        "students": students,
        "teacher_course": teacher_course,
    }
    return render(request, "teacher_template/teacher_edit_student.html", context)


@require_POST
def teacher_do_edit_grade(request):
    try:
        user = request.user
        teacher = Teacher.objects.get(user=user)
        grade = request.POST.get("grade")
        student_id = request.POST.get("student_id")
        student = get_object_or_404(Student, id=student_id)
        student_grade = StudentGrade.objects.get(student=student)
        student_grade.grade = grade
        student_grade.course = teacher.course
        student_grade.from_teacher = teacher
        student_grade.save()
        return redirect(reverse("teacher_edit_student"))
    except Exception as e:
        return HttpResponse("表单有错误", request)


@require_POST
def teacher_do_edit_evaluation(request):
    try:
        evaluation = request.POST.get("evaluation")
        student_id = request.POST.get("student_id")
        student = get_object_or_404(Student, id=student_id)
        student_grade = StudentGrade.objects.get(student=student)
        student_grade.teacher_evaluation = evaluation
        student_grade.save()
        return redirect(reverse("teacher_edit_student"))
    except Exception as e:
        return HttpResponse("表单有错误", request)


def teacher_view_score(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    teacher_grade = TeacherGrade.objects.filter(teacher=teacher)
    teacher_course = Course.objects.get(teacher=teacher)
    context = {
        "teacher_grade": teacher_grade,
        "teacher_course": teacher_course
    }
    return render(request, 'teacher_template/teacher_view_grade.html', context)


def teacher_view_analysis(request):
    teachers = Teacher.objects.all()
    sum_score = 0
    count = 0
    teacher_avg_scores = []
    teacher_name = []
    for teacher in teachers:
        teacher_grade = TeacherGrade.objects.filter(teacher=teacher)
        for grade in teacher_grade:
            count += 1
            sum_score += grade.grade
        if count == 0:
            avg_score = 0
        else:
            avg_score = sum_score / count
        teacher_avg_scores.append(avg_score)
        teacher_name.append(teacher.user.username)

        count = 0
        sum_score = 0
    this_teacher = Teacher.objects.get(user=request.user)
    this_teacher_grades = TeacherGrade.objects.filter(teacher=this_teacher)
    context = {
        "teacher_avg_scores": teacher_avg_scores,
        "teacher_name": teacher_name,
        "teacher_grades": this_teacher_grades,
    }
    return render(request, "teacher_template/data_visualize.html", context)


def student_view_profile(request):
    user = request.user
    student = Student.objects.get(user=user)
    recent_score_all = StudentGrade.objects.filter(student=student)
    all_score = 0
    all_course = 0
    for score in recent_score_all:
        all_score += score.grade
        all_course += 1
    if all_course == 0:
        average_score = 0
    else:
        average_score = all_score / all_course
    context = {
        'user': request.user,
        "average_score": average_score,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, "student_template/student_view_profile.html", context)


def student_edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "GET":
        user_form = UserForm(instance=student)
        change_password_form = ChangePasswordForm(user=student)
        change_email_form = ChangeEmailForm()
        context = {
            'user_form': user_form,
            "change_password_form": change_password_form,
            "change_email_form": change_email_form,
        }
        return render(request, "student_template/student_edit_profile.html", context)
    else:
        user_form = UserForm(request.POST, instance=student)
        if user_form.is_valid():
            username = user_form.cleaned_data.get("username")
            gender = user_form.cleaned_data.get("gender")
            self = user_form.cleaned_data.get("self")
            user = request.user
            user.username = username
            user.gender = gender
            user.self = self

            user.save()
            return redirect(reverse("edit_student_profile"))
        else:
            return redirect(reverse("edit_student_profile"))


def student_evaluate_teacher(request):
    teachers = Teacher.objects.all()
    student = Student.objects.get(user=request.user)
    context = {
        'teachers': teachers,
        "student": student,
    }
    return render(request, "student_template/student_evaluate_teacher.html", context)


@require_POST
def student_do_evaluate(request):
    try:
        teacher_id = request.POST.get("teacher_id")
        student_id = request.POST.get("from_student")
        teacher = Teacher.objects.get(id=teacher_id)
        student = Student.objects.get(id=student_id)
        grade = request.POST.get("teacher_score")
        student_advice = request.POST.get("teacher_advice")
        teacher_grade = TeacherGrade.objects.create(teacher=teacher, course=student.course, from_student=student,
                                                    grade=grade)
        teacher_grade.student_evaluation = student_advice
        teacher_grade.save()
        return redirect(reverse("student_evaluate_teacher"))
    except Exception as e:
        return HttpResponse("表单有误" + str(e), request)


def student_view_grade(request):
    student = Student.objects.get(user=request.user)
    student_grade_set = StudentGrade.objects.filter(student=student)
    context = {
        "student_grade": student_grade_set
    }
    return render(request, "student_template/student_view_grade.html", context)


def student_view_analysis(request):
    student_grades = StudentGrade.objects.filter(student=request.user.student)
    labels = []
    scores = []
    for grade in student_grades:
        labels.append(grade.course.course_name)
        scores.append(grade.grade)
    context = {
        "labels": labels,
        "scores": scores
    }
    return render(request, "student_template/data_visualize.html", context)


"""
更新如下：添加用户类型==2的用户 manager用户
功能：
编辑查看个人信息
管理学生，教师
添加课程
"""


def manager_home(request):
    """
    展示学生总数，课程总数，教师总数
    """
    all_student = Student.objects.all().count()
    all_course = Course.objects.all().count()
    all_teacher = Teacher.objects.all().count()
    context = {
        "all_student": all_student,
        "all_course": all_course,
        "all_teacher": all_teacher
    }
    return render(request, "manager_template/manager_home.html", context)


def manager_view_profile(request):
    user = request.user
    context = {
        'user':user
    }
    return render(request,"manager_template/manager_view_profile.html",context)

def manager_edit_profile(request):
    manager = Manager.objects.get(user=request.user)
    if request.method == "GET":
        user_form = UserForm(instance=manager)
        change_password_form = ChangePasswordForm(request.user)
        change_email_form = ChangeEmailForm()
        context = {
            'user_form': user_form,
            "change_password_form": change_password_form,
            "change_email_form": change_email_form,
        }
        return render(request, "manager_template/manager_edit_profile.html", context)
    else:
        user_form = UserForm(request.POST, instance=manager)
        if user_form.is_valid():
            username = user_form.cleaned_data.get("username")
            gender = user_form.cleaned_data.get("gender")
            self = user_form.cleaned_data.get("self")
            user = request.user
            user.username = username
            user.gender = gender
            user.self = self

            user.save()
            return redirect(reverse("manager_edit_profile"))
        else:
            return redirect(reverse("manager_edit_profile"))


def manager_change_password(request):
    manager = Manager.objects.get(user=request.user)
    if request.method == "POST":
        password_form = ChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            new_password = password_form.cleaned_data.get("new_password1")
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "修改成功")
            return redirect(reverse("manager_edit_profile"))
        else:
            errors = password_form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
            return redirect(reverse("manager_edit_profile"))
    return redirect(reverse("manager_edit_profile"), locals())


def manager_change_email(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get("email")
            user = request.user
            user.email = email
            user.save()
            messages.success(request, "修改成功")
            return redirect(reverse("manager_edit_profile"))
        else:
            errors = email_form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
            return redirect(reverse("manager_edit_profile"))
    return redirect(reverse("manager_edit_profile"), locals())


def manager_view_student(request):
    students = Student.objects.all()
    edit_student_username_form = EditUsernameForm()
    edit_student_email_form = EditEmailForm()
    context = {
        'students':students,
        'username_form':edit_student_username_form,
        'email_form':edit_student_email_form
    }
    return render(request,"manager_template/manager_view_student.html",context=context)

def manager_edit_student_username(request):
    student_id = request.POST.get('student_id')
    username = request.POST.get('username')
    user = CustomUser.objects.get(student__id = student_id)
    #valid
    if CustomUser.objects.filter(username = username).exists():
        messages.error(request,'该用户名已被注册!')
        return redirect("manager_view_student")
    user.username = username
    user.save()
    messages.success(request,"修改用户名成功!")
    return redirect('manager_view_student')

def manager_edit_student_email(request,student_id):
    student_id = request.POST.get('student_id')
    email = request.POST.get('email')
    user = CustomUser.objects.get(student__id=student_id)
    # valid
    if CustomUser.objects.filter(email=email).exists():
        messages.error(request, '该邮箱已被注册!')
        return redirect("manager_view_student")
    user.email = email
    user.save()
    messages.success(request, "修改邮箱成功!")
    return redirect('manager_view_student')


def manager_delete_student(request,student_id):
    student = get_object_or_404(CustomUser,student__id=student_id)
    student.delete()
    messages.success(request,f"删除学生 {student.username} 成功!")
    return redirect(reverse("manager_view_student"))


def manager_view_teacher(request):
    teachers = Teacher.objects.all()
    edit_teacher_username_form = EditUsernameForm()
    edit_teacher_email_form = EditEmailForm()
    context = {
        'teachers': teachers,
        'username_form': edit_teacher_username_form,
        'email_form': edit_teacher_email_form
    }
    return render(request, "manager_template/manager_view_teacher.html", context=context)


def manager_edit_teacher_username(request):
    teacher_id = request.POST.get('teacher_id')
    username = request.POST.get('username')
    user = CustomUser.objects.get(teacher__id = teacher_id)
    # valid
    if CustomUser.objects.filter(username = username).exists():
        messages.error(request, '该用户名已被注册!')
        return redirect("manager_view_teacher")
    user.username = username
    user.save()
    messages.success(request, "修改用户名成功!")
    return redirect('manager_view_teacher')


def manager_edit_teacher_email(request):
    teacher_id = request.POST.get('teacher_id')
    email = request.POST.get('email')
    user = CustomUser.objects.get(teacher__id = teacher_id)
    # valid
    if CustomUser.objects.filter(email=email).exists():
        messages.error(request, '该邮箱已被注册!')
        return redirect("manager_view_teacher")
    user.email = email
    user.save()
    messages.success(request, "修改邮箱成功!")
    return redirect('manager_view_teacher')

def manager_delete_teacher(request,teacher_id):
    teacher = get_object_or_404(CustomUser,teacher__id=teacher_id)
    teacher.delete()
    messages.success(request, f"删除教师 {teacher.username} 成功!")
    return redirect(reverse("manager_view_teacher"))

class reset_password(View):
    def get(self,request):
        return render(request,"main_template/reset_password.html")
    def post(self,request):
        #valid
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            user.set_password('123456')
            user.save()
            messages.success(request, "重置密码成功为123456")
            return redirect(reverse("reset_password"))
        except CustomUser.DoesNotExist:
            messages.error(request,"该用户名不存在!")
            return redirect(reverse('reset_password'))
