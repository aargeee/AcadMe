# Create your models here.
from django.db import models
from AcadMe.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from iam.models import AppUser

USER = get_user_model()


class Course(BaseModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)


class Enrollment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    learner = models.ForeignKey(USER, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.learner.role != AppUser.ROLES.LEARNER:
            raise ValueError("Only Students can enroll in a course.")
        super().save(*args, **kwargs)


class CourseTutor(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(USER, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.tutor.role != AppUser.ROLES.TUTOR:
            raise ValueError("Only Students can enroll in a course.")
        super().save(*args, **kwargs)


class Chapter(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.SmallIntegerField(blank=False, null=False)
    isLastChapter = models.BooleanField(default=False)


class Content(BaseModel):
    class ContentType(models.TextChoices):
        TEXT = "TEXT", _("TEXT")
        VIDEO = "VIDEO", _("VIDEO")
        BOTH = "BOTH", _("BOTH")

    name = models.CharField(max_length=64)
    type = models.CharField(choices=ContentType.choices)
    textUrl = models.URLField()
    videoUrl = models.URLField()
    position = models.SmallIntegerField(blank=False, null=False)
    isLastContent = models.BooleanField(default=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class TopicCompletionLog(BaseModel):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    learner = models.ForeignKey(USER, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.learner.role != AppUser.ROLES.LEARNER:
            raise ValueError("Only Students can enroll in a course.")
        super().save(*args, **kwargs)
