# Create your models here.
from django.db import models
from AcadMe.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from iam.models import AppUser
from django.core.exceptions import ValidationError

USER = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return f"Category {self.name}"

    class Meta:
        default_permissions = ()
        permissions = (
            ("add_category", "Create Category"),
            ("view_category", "View Category"),
            ("change_category", "Update Category"),
            ("delete_category", "Delete Category"),
        )


class Course(BaseModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return f"Course {self.name}"

    class Meta:
        default_permissions = ()
        permissions = (
            ("add_course", "Create Course"),
            ("view_course", "View Course"),
            ("change_course", "Update Course"),
            ("delete_course", "Delete Course"),
        )


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
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "position"], name="unique_position_per_course"
            )
        ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.SmallIntegerField(blank=False, null=False)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.course.name} > {self.name}"


class Content(BaseModel):
    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter", "position"], name="unique_position_per_chapter"
            )
        ]

    class TYPES(models.TextChoices):
        HTML = "HTML",_("HTML")
        VIDEO = "VIDEO",_("VIDEO")

    name = models.CharField(max_length=64)
    content = models.TextField()
    type = models.CharField(choices=TYPES.choices)
    position = models.SmallIntegerField(blank=False, null=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.type == self.TYPES.VIDEO:
            from django.core.validators import URLValidator
            url_validator = URLValidator()
            try:
                url_validator(self.content)
            except ValidationError:
                raise ValidationError({'content': _('Content must be a valid URL for VIDEO type.')})


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.chapter.name} > {self.name}"


class ContentCompletionLog(BaseModel):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    learner = models.ForeignKey(USER, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.learner.role != AppUser.ROLES.LEARNER:
            raise ValueError("Only Students can enroll in a course.")
        if not Enrollment.objects.filter(course=self.content.chapter.course, learner=self.learner).exists():
            raise ValidationError("Learner is not enrolled in the course related to this content.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.content.name} > {self.learner.get_username()}"

    class Meta:
        default_permissions = ()
        permissions = (
            ("add_completionlog", "Create Completion Log"),
            ("view_completionlog", "View Completion Log"),
            ("change_completionlog", "Update Completion Log"),
            ("delete_completionlog", "Delete Completion Log"),
        )
