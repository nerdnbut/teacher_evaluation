from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

# manager


# 创建自定义模型

class CustomUser(AbstractUser):
    username = models.CharField(max_length=12, unique=True)
    USER_TYPE = ((0, 'student'), (1, 'teacher'),(2,'manager'))
    GENDER = ((0, 'male'), (1, 'female'))
    email = models.EmailField()
    user_type = models.IntegerField(default=0, choices=USER_TYPE)
    gender = models.IntegerField(default=0, choices=GENDER)
    profile = models.ImageField()
    self = models.CharField(max_length=150, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Course(models.Model):
    course_name = models.CharField(max_length=128)

    def __str__(self):
        return self.course_name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, default=1)


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.DO_NOTHING, null=True)


#第三类用户 超级用户，管理学生，教师，课程
class Manager(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)



class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    from_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1)
    grade = models.FloatField()
    teacher_evaluation = models.CharField(max_length=150, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TeacherGrade(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    from_student = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField()
    student_evaluation = models.CharField(max_length=150, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created=False, **kwargs):
    if created:
        if instance.user_type == 0:
            student = Student.objects.create(user=instance)
            student.save()
        elif instance.user_type == 1:
            teacher = Teacher.objects.create(user=instance)
            teacher.save()
        else:
            manager = Manager.objects.create(user=instance)
            manager.save()


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 0:
        instance.student.save()
    elif instance.user_type == 1:
        instance.teacher.save()
    else:
        instance.manager.save()
