# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppUser(AbstractUser):
    class ROLES(models.TextChoices):
        ADMIN = "ADMIN", _("ADMIN")
        TUTOR = "TUTOR", _("TUTOR")
        LEARNER = "LEARNER", _("LEARNER")

    role = models.CharField(choices=ROLES.choices, default=ROLES.ADMIN)
