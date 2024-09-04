from django.contrib import admin

from main_app.models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(StudentGrade)
admin.site.register(TeacherGrade)
admin.site.register(CustomUser)