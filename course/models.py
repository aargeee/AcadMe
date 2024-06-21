# Create your models here.
from django.db import models
from AcadMe.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from iam.models import AppUser
from django.core.exceptions import ValidationError

USER = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Category {self.name}"


class Course(BaseModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return f"Course {self.name}"


class Enrollment(BaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "learner"], name="unique_learner_in_course"
            )
        ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    learner = models.ForeignKey(USER, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.learner.role != AppUser.ROLES.LEARNER:
            raise ValueError("Only Students can enroll in a course.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.course.name} - {self.learner.get_username()}"


class CourseTutor(BaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "tutor"], name="unique_tutor_in_course"
            )
        ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(USER, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.tutor.role != AppUser.ROLES.TUTOR:
            raise ValueError("Only Students can enroll in a course.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.course.name} - {self.tutor.get_username()}"


class Chapter(BaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "position"], name="unique_position_per_course"
            )
        ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.SmallIntegerField(blank=False, null=False)
    isLastChapter = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.course.name} > {self.name}"


class Content(BaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["chapter", "position"], name="unique_position_per_chapter"
            )
        ]

    class ContentType(models.TextChoices):
        TEXT = "TEXT", _("TEXT")
        VIDEO = "VIDEO", _("VIDEO")
        BOTH = "BOTH", _("BOTH")

    name = models.CharField(max_length=64)
    type = models.CharField(choices=ContentType.choices)
    textUrl = models.URLField(blank=True)
    videoUrl = models.URLField(blank=True)
    position = models.SmallIntegerField(blank=False, null=False)
    isLastContent = models.BooleanField(default=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def clean(self):
        super().clean()

        if self.type == self.ContentType.TEXT and not self.textUrl:
            raise ValidationError(
                {"textUrl": _("Text URL is required when content type is TEXT.")}
            )
        if self.type == self.ContentType.VIDEO and not self.videoUrl:
            raise ValidationError(
                {"videoUrl": _("Video URL is required when content type is VIDEO.")}
            )
        if self.type == self.ContentType.BOTH:
            if not self.textUrl:
                raise ValidationError(
                    {"textUrl": _("Text URL is required when content type is BOTH.")}
                )
            if not self.videoUrl:
                raise ValidationError(
                    {"videoUrl": _("Video URL is required when content type is BOTH.")}
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.chapter.name} > {self.name}"


class TopicCompletionLog(BaseModel):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    learner = models.ForeignKey(USER, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.learner.role != AppUser.ROLES.LEARNER:
            raise ValueError("Only Students can enroll in a course.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.content.name} > {self.learner.get_username()}"
