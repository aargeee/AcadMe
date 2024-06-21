# Register your models here.
from django.contrib import admin
from .models import (
    Content,
    Enrollment,
    CourseTutor,
    Chapter,
    Course,
    ContentCompletionLog,
    Category,
)

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(CourseTutor)
admin.site.register(Chapter)
admin.site.register(Content)
admin.site.register(ContentCompletionLog)
