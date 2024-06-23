# lib imports
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from iam.models import AppUser
from course.models import *
from django.db.models.functions import Cast
from django.db.models import DateField, Count

USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TutorSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = AppUser(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=AppUser.ROLES.TUTOR,
            is_staff=False,
            is_active=True,
        )
        user.set_password(validated_data["password"])
        user.save()

        # Clear any default groups and add user to 'tutor' group
        user.groups.clear()
        group = Group.objects.get(name="tutor")
        user.groups.add(group)

        return user


class LearnerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = AppUser(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=AppUser.ROLES.LEARNER,
            is_staff=False,
            is_active=True,
        )
        user.set_password(validated_data["password"])
        user.save()

        user.groups.clear()
        group = Group.objects.get(name="learner")
        user.groups.add(group)

        # Clear any default groups and add user to 'learner' group
        return user

class TutorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ["id", "username", "first_name", "last_name"]
        
class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ["id", "name", "description", "category_name"]
    def get_category_name(self, obj):
        return obj.category.name

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ["course"]

class ContentCompletionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCompletionLog
        fields = ["content", "created_at"]

class LearnerProfileSerializer(serializers.ModelSerializer):
    enrolled_courses = EnrollmentSerializer(many=True, source="enrollment_set")
    content_completion_by_date = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = ["id", "username", "first_name", "last_name", "enrolled_courses", "content_completion_by_date"]

    def get_content_completion_by_date(self, obj):
        # Get count of content completed each day
        completion_logs = (
            ContentCompletionLog.objects
            .filter(learner=obj)
            .annotate(date=Cast('created_at', DateField()))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        # Format the data for easy consumption
        return {log['date'].strftime('%Y-%m-%d'): log['count'] for log in completion_logs}