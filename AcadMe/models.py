# package imports
import uuid
from django.contrib.auth import get_user_model

# lib imports
from django.db import models
from django.utils.translation import gettext_lazy as _

USER = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("Modified At"), auto_now=True)
    created_by = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_created_by_user",
        default=None,
    )
    modified_by = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_modified_by_user",
        default=None,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        default_permissions = ()

    def created_by_name(self):
        if self.created_by:
            return self.created_by.get_full_name()
        else:
            return None

    def modified_by_name(self):
        if self.modified_by:
            return self.modified_by.get_full_name()
        else:
            return None
