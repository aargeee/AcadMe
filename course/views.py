# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Course
from .serializers import CourseSerializer, CourseDetailSerializer
from AcadMe.permissions import HasPermission

from django.shortcuts import get_object_or_404

from uuid import UUID


class CourseView(APIView):
    permission_classes = [HasPermission]
    permission_dict = {"POST": ["add_course"]}

    def get(self, _request: Request) -> Response:
        courseList = Course.objects.all()
        serialized = CourseSerializer(courseList, many=True)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serialized = CourseSerializer(data=request.data)
        if not serialized.is_valid():
            raise ValidationError(detail=serialized.errors)
        course: Course = serialized.save(created_by=request.user)
        response = {"success": True, "data": {"course_id": course.id}}
        return Response(data=response, status=status.HTTP_201_CREATED)


class CourseDetailView(APIView):
    permission_classes = [HasPermission]
    permission_dict = {}

    def get(self, _request: Request, courseid: UUID) -> Response:
        course = get_object_or_404(Course, id=courseid)
        serialized = CourseDetailSerializer(course)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)
