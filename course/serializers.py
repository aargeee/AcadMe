from rest_framework import serializers

from .models import Course


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
