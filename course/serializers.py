from rest_framework import serializers

from .models import Course, Content, Chapter, CourseTutor, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "description", "category"]


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "name", "fileUrl", "position"]


class ChapterSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, read_only=True, source="content_set")

    class Meta:
        model = Chapter
        fields = ["id", "name", "position", "content"]


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class CourseTutorSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(read_only=True)

    class Meta:
        model = CourseTutor
        fields = ["tutor"]


class CourseDetailSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True, source="chapter_set")
    tutors = serializers.SerializerMethodField()
    enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "category",
            "chapters",
            "tutors",
            "enrolled_count",
        ]

    def get_tutors(self, obj):
        tutors = CourseTutor.objects.filter(course=obj)
        return CourseTutorSerializer(tutors, many=True).data

    def get_enrolled_count(self, obj):
        return Enrollment.objects.filter(course=obj).count()
