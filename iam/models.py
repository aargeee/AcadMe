# lib imports
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        Normal user creation.
        Returns: User instance
        """
        if not username:
            raise ValueError(_("The Username must be set"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Superuser creation.
        Returns User instance
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username, password, **extra_fields)


# custom user model.
class AppUser(AbstractBaseUser, PermissionsMixin):
    # Default Fields
    # AbstractBaseUser: password and last_login.
    # PermissionsMixin: is_superuser, groups and user_permissions.

    username_validator = UnicodeUsernameValidator(
        regex=r"^[a-zA-Z0-9_]+$",
        message="Enter a valid username. This value may contain only letters, numbers, and _ character.",
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    class ROLES(models.TextChoices):
        ADMIN = "ADMIN", _("ADMIN")
        TUTOR = "TUTOR", _("TUTOR")
        LEARNER = "LEARNER", _("LEARNER")

    role = models.CharField(max_length=10, choices=ROLES.choices, default=ROLES.ADMIN)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = ()
        permissions = (
            ("add_user", "Create user"),
            ("view_user", "View user"),
            ("change_user", "Update user"),
            ("delete_user", "Delete user"),
            ("add_role", "Create role"),
            ("view_role", "View role"),
            ("change_role", "Update role"),
            ("delete_role", "Delete role"),
        )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
