from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Generate learner and tutor groups"

    def handle(self, *args: Any, **options: Any) -> str | None:
        if Group.objects.filter(name="learner") is None:
            learner_group = Group(name="learner")
            learner_group.save()
            print("learner group created")
        else:
            print("learner group detected")

        if Group.objects.filter(name="tutor") is None:
            tutor_group = Group(name="tutor")
            tutor_group.save()
            print("tutor group created")
        else:
            print("tutor group detected")
